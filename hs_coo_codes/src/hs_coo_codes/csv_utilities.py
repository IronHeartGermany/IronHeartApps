"""
Utilities for CSV files
"""

import logging

from .coo_codes import (COOCodes,
                        COO_CODES_CHINA,
                        COO_CODES_GERMANY,
                        COO_CODES_GREAT_BRITAIN,
                        COO_CODES_JAPAN,
                        COO_CODES_SINGAPORE,
                        COO_CODES_USA)
from .columns import header_map, InventoryColumns, Field

def validate_header(header: list[str]) -> bool:
    """ Validate the header in the CSV file """

    # Validate header length
    header_length = len(header)
    expected_header_length = len(InventoryColumns)
    if header_length not in (expected_header_length, expected_header_length - 1):
        logging.error("Observed %s header columns but expected %s or %s header columns",
                      len(header),
                      expected_header_length,
                      expected_header_length - 1)
        return False

    # Validate each entry in the header
    for column in range(header_length):
        expected_title, _ = header_map[column]
        if header[column] != expected_title:
            logging.error("Observed header field %s in column %d but expected %s",
                          header[column], column, expected_title)
            return False

    return True


def validate_row(row_number: int,
                 header_length: int,
                 row: list[str],
                 check_hs: bool,
                 check_coo: bool,
                 check_us_hts: bool) -> bool:
    """
    Validate a row in the CSV file by checking if row length is same as header length
    and entries exist or do not exist depending on the expectations.
    """

    row_length = len(row)

    if row_length != header_length:
        logging.error("Header has length %d but row %d has length %d",
                      header_length, row_number, row_length)
        return False

    for column in range(row_length):
        if not check_hs and column == InventoryColumns.HS_CODE.value:
            continue
        if not check_coo and column == InventoryColumns.COO.value:
            continue
        if not check_us_hts and column == InventoryColumns.US_HTS_CODE.value:
            continue

        title, field_required = header_map[column]
        if row[column] and field_required == Field.EMPTY:
            logging.error("(Row %d Column %s) has value %s but was expected to be empty",
                          row_number, title, row[column])
            return False
        if not row[column].strip() and field_required == Field.REQUIRED:
            logging.error("(Row %d Column %s) does not have a value but is expected to have one",
                          row_number, title)
            return False
    return True


def create_header(header: list[str]) -> list[str]:
    """Create a header, including the US HTS Field"""
    new_header = header[:]
    new_header.append(header_map[InventoryColumns.US_HTS_CODE][0])
    return new_header


def create_row_with_codes(row_number: int, row: list[str]) -> list[str] | None:
    """Given a row, create a new row with HS and COO codes"""
    new_row = row[:]

    sku = row[InventoryColumns.SKU]

    if not sku:
        # Handle products without an SKU
        hs_code = "AAA"
        us_hts_code = "BBB"

        title = row[InventoryColumns.TITLE]
        coo_code = get_coo_from_sku(title.split("-", 1)[0], False)
        if coo_code is None:
            coo_code = get_coo_from_title(title.split(" ", 1)[0].strip())
    else:
        # Handle products with an SKU
        hs_code = "AAA"
        us_hts_code = "BBB"
        coo_code = get_coo_from_sku(sku.split("-", 1)[0])

    if hs_code is None:
        logging.error("Generated HS Code of None for row %d", row_number)
        return None
    if coo_code is None:
        logging.error("Generated COO Code of None for row %d", row_number)
        return None
    if us_hts_code is None:
        logging.error("Generated US HTS Code of None for row %d", row_number)
        return None

    # Check if existing COO code does not match current COO code
    if row[InventoryColumns.COO] and coo_code != row[InventoryColumns.COO]:
        logging.warning("COO code %s does not match existing code %s in row %d (SKU=%s)",
                        coo_code, row[InventoryColumns.COO], row_number, row[InventoryColumns.SKU])

    new_row[InventoryColumns.HS_CODE] = hs_code
    new_row[InventoryColumns.COO] = coo_code
    new_row.append(us_hts_code)

    return new_row

def get_coo_from_sku(sku_start: str, log: bool=True) -> str | None:
    """Get the COO from the SKU"""
    if sku_start in COO_CODES_CHINA:
        coo = COOCodes.CHINA.value
    elif sku_start in COO_CODES_GERMANY:
        coo = COOCodes.GERMANY.value
    elif sku_start in COO_CODES_GREAT_BRITAIN:
        coo =  COOCodes.GREAT_BRITAIN.value
    elif sku_start in COO_CODES_JAPAN:
        coo = COOCodes.JAPAN.value
    elif sku_start in COO_CODES_SINGAPORE:
        coo = COOCodes.SINGAPORE.value
    elif sku_start in COO_CODES_USA:
        coo = COOCodes.USA.value
    else:
        if log:
            logging.error("Could not map SKU-Start '%s' to COO", sku_start)
        coo = None
    return coo

def get_coo_from_title(title: str) -> str | None:
    """Get the COO from the Title"""
    title_start = title.split(" ", 1)[0].strip()
    if title_start in ("Rats", "Trophy"):
        return COOCodes.JAPAN

    logging.error("Could not map title '%s' to COO", title)
    return None
