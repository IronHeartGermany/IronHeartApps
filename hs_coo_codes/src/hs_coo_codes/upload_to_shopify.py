'''
Upload COO and HS Codes to Shopify via the Shopify API.
'''

import csv
import logging
import sys

from typing import NamedTuple

import click

from .columns import InventoryColumns
from . import csv_utilities

class Codes(NamedTuple):
    """COO, HS, and US HTS Codes"""
    coo: str | None
    hs: str | None
    us_hts: str | None


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

        # Get mapping from sku to a list of (id, codes) from Shopify
        shopify_sku_to_items = _get_shopify_sku_to_items()
        if shopify_sku_to_items is None:
            return False

        # Create dictionary from inventory IDs to codes (used to upload codes)
        shopify_id_to_codes = _create_id_to_codes(csv_sku_to_codes, shopify_sku_to_items)

        # Upload codes to Shopify
        if not _upload_codes_to_shopify(shopify_id_to_codes):
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
        logging.warning("%d rows do not have an SKU", num_rows_without_sku)
    return sku_to_codes


def _get_shopify_sku_to_items() -> dict[str, list[tuple[str, Codes]]] | None:
    """Get a dictionary from sku to a list of (inventory_item_id, codes) from Shopify"""
    # TODO: Implement

    return None


def _create_id_to_codes(csv_sku_to_codes: dict[str, Codes],
                        shopify_sku_to_items: dict[str, list[tuple[str, Codes]]]
                        ) -> dict[str, Codes]:
    """Create a dictionary from inventory item id to codes to upload"""
    id_to_codes: dict[str, Codes] = {}
    for (sku, csv_codes) in csv_sku_to_codes.items():
        if sku not in shopify_sku_to_items:
            logging.warning("SKU %s in CSV but not Shopify - cannot upload", sku)
        else:
            for (shopify_id, shopify_codes) in shopify_sku_to_items[sku]:
                if csv_codes != shopify_codes:
                    id_to_codes[shopify_id] = csv_codes

    return id_to_codes


def _upload_codes_to_shopify(id_to_codes: dict[str, Codes]) -> bool:
    # TODO: Implement
    for (shopify_id, codes) in id_to_codes.items():
        pass

    return True


if __name__ == "__main__":
    cli.main()
