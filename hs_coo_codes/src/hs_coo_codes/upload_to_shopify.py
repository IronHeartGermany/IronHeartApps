'''
Upload COO and HS Codes to Shopify via the Shopify API.
'''

import csv
import logging
import os
import sys
import time

from typing import NamedTuple

import click
import requests

from .columns import InventoryColumns
from .coo_codes import COOCodes
from . import csv_utilities

class Codes(NamedTuple):
    """COO, HS, and US HTS Codes"""
    coo: str | None
    hs: str | None
    us_hts: str | None


API_VERSION = "2026-10"
PAGE_SIZE = 100
MAX_THROTTLE_RETRIES = 3

VARIANTS_QUERY = """
query ($cursor: String, $pageSize: Int!) {
  productVariants(first: $pageSize, after: $cursor) {
    pageInfo { hasNextPage endCursor }
    nodes {
      sku
      inventoryItem {
        id
        countryCodeOfOrigin
        harmonizedSystemCode
        countryHarmonizedSystemCodes(first: 10) {
          pageInfo { hasNextPage }
          nodes { countryCode harmonizedSystemCode }
        }
      }
    }
  }
}
"""


@click.command()
@click.option('--input-file', required=True, type=click.Path(exists=True),
              help="Input CSV file containing COO, HS, and US-HTS Codes")
def cli(input_file):
    """Main function"""

    logging.basicConfig(level=logging.INFO)

    if upload_to_shopify(input_file):
        logging.info("Upload to Shopify successful")
    else:
        logging.critical("Upload to Shopify failed")
        sys.exit(1)


def upload_to_shopify(input_file: str) -> bool:
    """Upload COO, HS, and US-HTS Codes to Shopify"""
    try:
        with open(input_file, 'r', encoding='utf-8', newline="") as f:
            reader = csv.reader(f)
            header = next(reader)
            if not csv_utilities.validate_header(header):
                logging.error("Header validation failed")
                return False
            if len(header) != len(InventoryColumns):
                logging.error("Header too short (check if US HTS is included)")
                return False

            # Get mapping from sku to codes from the CSV
            csv_sku_to_codes = _get_csv_sku_to_codes(reader, len(header))
            if csv_sku_to_codes is None:
                return False

        # Connect to the Shopify Admin API
        connection = _create_session()
        if connection is None:
            return False
        session, graphql_url = connection

        # Get mapping from sku to a list of (id, codes) from Shopify
        shopify_sku_to_items = _get_shopify_sku_to_items(session, graphql_url)
        if shopify_sku_to_items is None:
            return False

        # Create dictionary from inventory IDs to codes (used to upload codes)
        shopify_id_to_codes, skipped_skus = _create_id_to_codes(csv_sku_to_codes, shopify_sku_to_items)
        if len(skipped_skus) > 0:
            return False

        # Upload codes to Shopify
        if not _upload_codes_to_shopify(session, graphql_url, shopify_id_to_codes):
            return False

    except (OSError, csv.Error, StopIteration) as e:
        logging.error("Upload to Shopify failed: %s", e)
        return False

    return True

def _get_csv_sku_to_codes(reader, row_length: int) -> dict[str, Codes] | None:
    """Get the dictionary from sku to codes from the CSV"""
    sku_to_codes: dict[str, Codes] = {}
    num_rows_without_sku = 0
    for index, row in enumerate(reader, start=2):
        if not csv_utilities.validate_row(index, row_length, row, check_hs=True,
                                          check_coo=True, check_us_hts=True):
            logging.error("Row validation failed for row %s", index)
            return None

        sku = row[InventoryColumns.SKU.value]
        coo = row[InventoryColumns.COO.value]
        hs = row[InventoryColumns.HS_CODE.value]
        us_hts = row[InventoryColumns.US_HTS_CODE.value]

        # Validate values that will be uploaded
        if coo not in COOCodes:
            logging.error("Invalid COO Code (%s) in row %d", coo, index)
            return None
        if not (len(us_hts) == 10 and us_hts.isdigit() and us_hts.isascii()):
            logging.error("US HTS Code (%s) is not 10-digit ASCII in row %d", us_hts, index)
            return None
        if not hs == us_hts[:6]:
            logging.error("HS Code (%s) is not first 6 digits of US HTS Code (%s) in row %d",
                          hs, us_hts, index)
            return None

        if not sku:
            num_rows_without_sku += 1
            continue

        if sku not in sku_to_codes:
            sku_to_codes[sku] = Codes(coo, hs, us_hts)
        else:
            existing_codes = sku_to_codes[sku]
            if existing_codes.coo != coo:
                logging.error("COO (%s) does not match existing COO (%s) for SKU %s",
                              coo, existing_codes.coo, sku)
                return None
            if existing_codes.hs != hs:
                logging.error("HS (%s) does not match existing HS (%s) for SKU %s",
                              hs, existing_codes.hs, sku)
                return None
            if existing_codes.us_hts != us_hts:
                logging.error("US HTS (%s) does not match existing US HTS (%s) for SKU %s",
                              us_hts, existing_codes.us_hts, sku)
                return None

    if num_rows_without_sku > 0:
        logging.warning("%d rows do not have an SKU in the CSV", num_rows_without_sku)
    return sku_to_codes


def _create_session() -> tuple[requests.Session, str] | None:
    """Get an access token and return a session using it and the GraphQL URL"""
    try:
        store = os.environ["SHOPIFY_STORE"]
        response = requests.post(f"https://{store}/admin/oauth/access_token", timeout=30, data={
            "grant_type": "client_credentials",
            "client_id": os.environ["SHOPIFY_CLIENT_ID"],
            "client_secret": os.environ["SHOPIFY_CLIENT_SECRET"]})
        response.raise_for_status()
        token = response.json()["access_token"]
    except KeyError as e:
        logging.error("Environment variable or access token %s missing", e)
        return None
    except (requests.RequestException, ValueError) as e:
        logging.error("Could not get Shopify access token: %s", e)
        return None

    session = requests.Session()
    session.headers["X-Shopify-Access-Token"] = token
    return session, f"https://{store}/admin/api/{API_VERSION}/graphql.json"


def _graphql(session: requests.Session, graphql_url: str, query: str,
             variables: dict) -> dict | None:
    """Run a GraphQL query and return its data, or None on any error.
    Throttled queries are retried up to MAX_THROTTLE_RETRIES times."""
    for attempt in range(MAX_THROTTLE_RETRIES + 1):
        try:
            response = session.post(graphql_url, json={"query": query, "variables": variables},
                                    timeout=60)
            response.raise_for_status()
            result = response.json()
        except (requests.RequestException, ValueError) as e:
            logging.error("Shopify GraphQL request failed: %s", e)
            return None

        cost = result.get("extensions", {}).get("cost", {})
        throttle = cost.get("throttleStatus")

        if "errors" in result:
            throttled = all(error.get("extensions", {}).get("code") == "THROTTLED"
                            for error in result["errors"])
            if (not throttled or throttle is None or "requestedQueryCost" not in cost
                    or attempt == MAX_THROTTLE_RETRIES):
                logging.error("Shopify GraphQL errors: %s", result["errors"])
                return None
            # Wait until the budget covers the requested cost, then retry
            wait = ((cost["requestedQueryCost"] - throttle["currentlyAvailable"])
                    / throttle["restoreRate"] + 1)
            logging.warning("Shopify query throttled (needs %d, %d available), "
                            "retrying in %.1f s", cost["requestedQueryCost"],
                            throttle["currentlyAvailable"], wait)
            time.sleep(max(wait, 1))
            continue

        # Wait if the query cost budget is running low
        if throttle and throttle["currentlyAvailable"] < throttle["maximumAvailable"] / 4:
            wait = ((throttle["maximumAvailable"] / 2 - throttle["currentlyAvailable"])
                    / throttle["restoreRate"])
            logging.info("Shopify query budget low (%d available), sleeping %.1f s",
                         throttle["currentlyAvailable"], wait)
            time.sleep(wait)

        return result["data"]

    return None


def _get_shopify_sku_to_items(session: requests.Session, graphql_url: str
                              ) -> dict[str, list[tuple[str, Codes]]] | None:
    """Get a dictionary from sku to a list of (inventory_item_id, codes) from Shopify"""
    sku_to_items: dict[str, list[tuple[str, Codes]]] = {}
    num_variants_without_sku = 0
    cursor = None
    while True:
        data = _graphql(session, graphql_url, VARIANTS_QUERY,
                        {"cursor": cursor, "pageSize": PAGE_SIZE})
        if data is None:
            return None
        variants = data["productVariants"]

        for variant in variants["nodes"]:
            sku = variant["sku"]
            if not sku:
                num_variants_without_sku += 1
                continue
            item = variant["inventoryItem"]
            country_codes = item["countryHarmonizedSystemCodes"]
            if country_codes["pageInfo"]["hasNextPage"]:
                logging.error("SKU %s has too many country HS codes to read the US code", sku)
                return None
            us_hts = None
            for country_code in country_codes["nodes"]:
                if country_code["countryCode"] == "US":
                    us_hts = country_code["harmonizedSystemCode"]
            codes = Codes(item["countryCodeOfOrigin"], item["harmonizedSystemCode"], us_hts)
            sku_to_items.setdefault(sku, []).append((item["id"], codes))

        if not variants["pageInfo"]["hasNextPage"]:
            break
        cursor = variants["pageInfo"]["endCursor"]

    if num_variants_without_sku > 0:
        logging.warning("%d variants do not have an SKU in Shopify", num_variants_without_sku)
    logging.info("Read %d SKUs from Shopify", len(sku_to_items))
    return sku_to_items


def _create_id_to_codes(csv_sku_to_codes: dict[str, Codes],
                        shopify_sku_to_items: dict[str, list[tuple[str, Codes]]]
                        ) -> tuple[dict[str, Codes], list[str]]:
    """Create a dictionary from inventory item id to codes to upload"""
    id_to_codes: dict[str, Codes] = {}
    skipped_skus = []
    for (sku, csv_codes) in csv_sku_to_codes.items():
        if sku not in shopify_sku_to_items:
            logging.warning("SKU %s in CSV but not Shopify - cannot upload", sku)
            skipped_skus.append(sku)
        else:
            for (shopify_id, shopify_codes) in shopify_sku_to_items[sku]:
                if csv_codes != shopify_codes:
                    id_to_codes[shopify_id] = csv_codes

    if not id_to_codes and len(skipped_skus) == 0:
        logging.info("Shopify already synced with CSV - nothing to upload")
    return id_to_codes, skipped_skus


def _upload_codes_to_shopify(session: requests.Session, graphql_url: str,
                             id_to_codes: dict[str, Codes]) -> bool:
    # TODO: Implement
    for (shopify_id, codes) in id_to_codes.items():
        pass

    return True


if __name__ == "__main__":
    cli.main()
