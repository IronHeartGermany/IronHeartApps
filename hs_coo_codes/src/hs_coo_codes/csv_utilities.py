"""
Utilities for CSV files
"""

import logging

from .columns import header_map, InventoryColumns, Field


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
