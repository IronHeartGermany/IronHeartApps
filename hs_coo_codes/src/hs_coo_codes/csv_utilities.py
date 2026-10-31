"""
Utilities for CSV files
"""

import logging

from .codes import (COOCodes,
                    COO_CODES_CHINA,
                    COO_CODES_GERMANY,
                    COO_CODES_GREAT_BRITAIN,
                    COO_CODES_JAPAN,
                    COO_CODES_SINGAPORE,
                    COO_CODES_USA)
from .columns import header_map, InventoryColumns, Field
from .sku import StartSKU


def validate_header(header: list[str]) -> bool:
    """ Validate the header in the CSV file """

    # Validate header length
    if len(header) != len(InventoryColumns):
        logging.error("Observed %s header columns but expected %s header columns",
                      len(header),
                      len(InventoryColumns))
        return False

    # Validate each entry in the header
    for column in InventoryColumns:
        expected_title, _ = header_map[column]
        if header[column.value] != expected_title:
            logging.error("Observed header field %s in column %d but expected %s",
                          header[column.value], column.value, expected_title)
            return False

    return True


def validate_row(row_number: int, row: list[str], check_hs: bool, check_coo: bool) -> bool:
    """
    Validate a row in the CSV file by checking if entries exist or do not exist
    depending on the expectations.
    """

    if len(row) != len(InventoryColumns):
        logging.error("Row %d has length %d but is expected to have length %d",
                      row_number, len(row), len(InventoryColumns))
        return False

    for column in InventoryColumns:
        if not check_hs and column == InventoryColumns.HS_CODE:
            continue
        if not check_coo and column == InventoryColumns.COO:
            continue

        title, field_required = header_map[column]
        if row[column.value] and field_required == Field.EMPTY:
            logging.error("(Row %d Column %s) has value %s but was expected to be empty",
                          row_number, title, row[column.value])
            return False
        if not row[column.value].strip() and field_required == Field.REQUIRED:
            logging.error("(Row %d Column %s) does not have a value but is expected to have one",
                          row_number, title)
            return False
    return True


def create_row_with_codes(row_number: int, row: list[str]) -> list[str] | None:
    """Given a row, create a new row with HS and COO codes"""
    new_row = row[:]

    sku = row[InventoryColumns.SKU.value]

    # Handle products without an SKU
    if not sku:
        hs_code = "AAA"
        coo_code = "BB"
    else:
        hs_code = "AAA"
        coo_code = get_coo_from_sku(sku.split("-", 1)[0])

    if hs_code is None:
        logging.error("Generated HS Code of None for row %d", row_number)
        return None
    if coo_code is None:
        logging.error("Generated COO Code of None for row %d", row_number)
        return None

    return new_row

def get_coo_from_sku(sku: str) -> str | None:
    """Get the COO from the SKU"""
    if sku in COO_CODES_CHINA:
        coo = COOCodes.CHINA
    elif sku in COO_CODES_GERMANY:
        coo = COOCodes.GERMANY
    elif sku in COO_CODES_GREAT_BRITAIN:
        coo = COOCodes.GREAT_BRITAIN
    elif sku in COO_CODES_JAPAN:
        coo = COOCodes.JAPAN
    elif sku in COO_CODES_SINGAPORE:
        coo = COOCodes.SINGAPORE
    elif sku in COO_CODES_USA:
        coo = COOCodes.USA
    else:
        logging.error("Could not map SKU-Start '%s' to COO", sku)
        coo = None

    return coo