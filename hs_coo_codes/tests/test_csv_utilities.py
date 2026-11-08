"""
Test the validation of the CSV utilities.
"""

import csv

from hs_coo_codes import coo_codes
from hs_coo_codes import csv_utilities


def test_short_header():
    """ Test that a CSV with a short header returns false in validate_inventory """
    with open("data/test/short_header.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert not csv_utilities.validate_header(header)

def test_bad_header_csv():
    """ Test that a CSV with a bad header returns false in validate_inventory """
    with open("data/test/bad_header.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert not csv_utilities.validate_header(header)

def test_empty_row_element_csv():
    """ Test that a CSV with an empty row element returns false in validate_inventory """
    with open("data/test/empty_row_element.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        row = next(reader)
        assert not csv_utilities.validate_row(2, row, False, False)

def test_row_too_short_csv():
    """ Test that a CSV with a short row returns false in validate_inventory """
    with open("data/test/short_row.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        row = next(reader)

        assert not csv_utilities.validate_row(2, row, False, False)

def test_missing_hs_code():
    """ Test that missing HS Codes returns false when not ignored """
    with open("data/test/missing_hs_code.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        row = next(reader)
        assert not csv_utilities.validate_row(2, row, True, False)

def test_space_as_hs_code():
    """ Test that a space as HS Code returns false when not ignored """
    with open("data/test/space_hs_code.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        row = next(reader)
        assert not csv_utilities.validate_row(2, row, True, False)

def test_missing_coo():
    """ Test that missing COO returns false when not ignored """
    with open("data/test/missing_coo.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        row = next(reader)
        assert not csv_utilities.validate_row(2, row, False, True)

def test_field_not_empty():
    """ Test a field that should be empty but is not returns false """
    with open("data/test/field_should_be_empty.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        row = next(reader)
        assert not csv_utilities.validate_row(2, row, False, False)

def test_missing_hs_code_ignored():
    """ Test that missing HS Codes returns true when ignored """
    with open("data/test/missing_hs_code.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        row = next(reader)
        assert csv_utilities.validate_row(2, row, False, False)

def test_missing_coo_ignored():
    """ Test that missing COO returns true when ignored """
    with open("data/test/missing_coo.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        row = next(reader)
        assert csv_utilities.validate_row(2, row, False, False)

def test_valid_csv():
    """ Test that a valid CSV returns True """
    with open("data/test/valid.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        row = next(reader)
        assert csv_utilities.validate_row(2, row, True, True)

def test_get_coo_codes_from_sku():
    """ Test getting the COO codes from the start of the SKUs """
    for sku_start in coo_codes.COO_CODES_CHINA:
        assert csv_utilities.get_coo_from_sku(sku_start) == coo_codes.COOCodes.CHINA
    for sku_start in coo_codes.COO_CODES_GERMANY:
        assert csv_utilities.get_coo_from_sku(sku_start) == coo_codes.COOCodes.GERMANY
    for sku_start in coo_codes.COO_CODES_GREAT_BRITAIN:
        assert csv_utilities.get_coo_from_sku(sku_start) == coo_codes.COOCodes.GREAT_BRITAIN
    for sku_start in coo_codes.COO_CODES_JAPAN:
        assert csv_utilities.get_coo_from_sku(sku_start) == coo_codes.COOCodes.JAPAN
    for sku_start in coo_codes.COO_CODES_SINGAPORE:
        assert csv_utilities.get_coo_from_sku(sku_start) == coo_codes.COOCodes.SINGAPORE
    for sku_start in coo_codes.COO_CODES_USA:
        assert csv_utilities.get_coo_from_sku(sku_start) == coo_codes.COOCodes.USA
    assert csv_utilities.get_coo_from_sku("INVALID") is None

def test_get_coo_from_title():
    """ Test getting the COO codes from the title """
    assert (csv_utilities.get_coo_from_title("Rats Monster Skull T-Shirt Black") ==
            coo_codes.COOCodes.JAPAN)
    assert (csv_utilities.get_coo_from_title("Trophy - Coke Stripe Pants 11 Oz Black") ==
            coo_codes.COOCodes.JAPAN)
    assert csv_utilities.get_coo_from_title("Invalid Title") is None

def test_create_row_with_codes():
    """ Test creating a row in the CSV with the codes """

    input_row = ['iron-heart-ih-666s-21-21oz-selvedge-denim-slim-straight-cut-jeans-indigo',
                 'IH-666S-21 - 21oz Selvedge Denim Slim Straight Cut Jeans - Indigo', 'Size',
                 '35', '', '', '', '', 'IH-666S-21', '', '', 'Hamburg Store IH Germany',
                 '', '0', '0', '0', '0', '0', '', '', '', '', ''
                 ]

    output_row = csv_utilities.create_row_with_codes(2, input_row)
    assert output_row is not None
    assert output_row[csv_utilities.InventoryColumns.HS_CODE] == "AAA"
    assert output_row[csv_utilities.InventoryColumns.COO] == csv_utilities.COOCodes.JAPAN.value

def test_create_row_with_codes_no_sku():
    """ Test creating a row in the CSV with the codes when there is no SKU """

    input_row = ['trophy-15th-anniversary-1605-jeans-standard-dirt-denim-14-5-oz',
                 'Trophy - 15th Anniversary 1605 Jeans 14,5 Oz Standard Dirt Denim',
                 'Size', '38', '', '', '', '', '', '', '',
                 'Kunden Reservierung Lager', '', '0', '0', '0', '0', '0', '', '',
                 '', '', '']

    output_row = csv_utilities.create_row_with_codes(2, input_row)
    assert output_row is not None
    assert output_row[csv_utilities.InventoryColumns.HS_CODE] == "AAA"
    assert output_row[csv_utilities.InventoryColumns.COO] == csv_utilities.COOCodes.JAPAN.value
