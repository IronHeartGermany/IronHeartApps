"""
Test the validation of the CSV utilities.
"""

import csv

import pytest

from hs_coo_codes import coo_codes
from hs_coo_codes import csv_utilities
from hs_coo_codes.hs_codes import HSCodes


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
        header = next(reader)
        row = next(reader)
        assert not csv_utilities.validate_row(2, len(header), row, False, False, False)

def test_row_too_short_csv():
    """ Test that a CSV with a short row returns false in validate_inventory """
    with open("data/test/short_row.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        row = next(reader)

        assert not csv_utilities.validate_row(2, len(header), row, False, False, False)

def test_missing_hs_code():
    """ Test that missing HS Codes returns false when not ignored """
    with open("data/test/missing_hs_code.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        row = next(reader)
        assert not csv_utilities.validate_row(2, len(header), row, True, False, False)

def test_space_as_hs_code():
    """ Test that a space as HS Code returns false when not ignored """
    with open("data/test/space_hs_code.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        row = next(reader)
        assert not csv_utilities.validate_row(2, len(header), row, True, False, False)

def test_missing_coo():
    """ Test that missing COO returns false when not ignored """
    with open("data/test/missing_coo.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        row = next(reader)
        assert not csv_utilities.validate_row(2, len(header), row, False, True, False)

def test_field_not_empty():
    """ Test a field that should be empty but is not returns false """
    with open("data/test/field_should_be_empty.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        row = next(reader)
        assert not csv_utilities.validate_row(2, len(header), row, False, False, False)

def test_missing_hs_code_ignored():
    """ Test that missing HS Codes returns true when ignored """
    with open("data/test/missing_hs_code.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        row = next(reader)
        assert csv_utilities.validate_row(2, len(header), row, False, False, False)

def test_missing_coo_ignored():
    """ Test that missing COO returns true when ignored """
    with open("data/test/missing_coo.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        row = next(reader)
        assert csv_utilities.validate_row(2, len(header), row, False, False, False)

def test_valid_csv():
    """ Test that a valid CSV returns True """
    with open("data/test/valid.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        row = next(reader)
        assert csv_utilities.validate_row(2, len(header), row, True, True, False)

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
    assert output_row[csv_utilities.InventoryColumns.HS_CODE] == "620342"
    assert output_row[csv_utilities.InventoryColumns.COO] == csv_utilities.COOCodes.JAPAN.value
    assert output_row[csv_utilities.InventoryColumns.US_HTS_CODE] == "6203424511"

def test_create_row_with_codes_has_us_hts():
    """ Test that an existing US HTS value is replaced, not appended """

    input_row = ['iron-heart-ih-666s-21-21oz-selvedge-denim-slim-straight-cut-jeans-indigo',
                 'IH-666S-21 - 21oz Selvedge Denim Slim Straight Cut Jeans - Indigo', 'Size',
                 '35', '', '', '', '', 'IH-666S-21', '', '', 'Hamburg Store IH Germany',
                 '', '0', '0', '0', '0', '0', '', '', '', '', '', '0123456789'
                 ]

    output_row = csv_utilities.create_row_with_codes(2, input_row)
    assert output_row is not None
    assert len(output_row) == len(csv_utilities.InventoryColumns)
    assert output_row[csv_utilities.InventoryColumns.HS_CODE] == "620342"
    assert output_row[csv_utilities.InventoryColumns.COO] == csv_utilities.COOCodes.JAPAN.value
    assert output_row[csv_utilities.InventoryColumns.US_HTS_CODE] == "6203424511"

def test_create_row_with_codes_no_sku():
    """ Test creating a row in the CSV with the codes when there is no SKU """

    input_row = ['trophy-15th-anniversary-1605-jeans-standard-dirt-denim-14-5-oz',
                 'Trophy - 15th Anniversary 1605 Jeans 14,5 Oz Standard Dirt Denim',
                 'Size', '38', '', '', '', '', '', '', '',
                 'Kunden Reservierung Lager', '', '0', '0', '0', '0', '0', '', '',
                 '', '', '']

    output_row = csv_utilities.create_row_with_codes(2, input_row)
    assert output_row is not None
    assert output_row[csv_utilities.InventoryColumns.HS_CODE] == "620342"
    assert output_row[csv_utilities.InventoryColumns.COO] == csv_utilities.COOCodes.JAPAN.value
    assert output_row[csv_utilities.InventoryColumns.US_HTS_CODE] == "6203424511"

def test_header_with_us_hts():
    """ Test that a header is generated with the US HTS CODE column """
    with open("data/test/valid.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        new_header = csv_utilities.create_header(header)
        assert len(header) == csv_utilities.InventoryColumns.US_HTS_CODE.value
        assert len(new_header) == csv_utilities.InventoryColumns.US_HTS_CODE.value + 1
        assert csv_utilities.validate_header(header)
        assert csv_utilities.validate_header(new_header)

def test_header_having_us_hts():
    """ Test that a header is not generated with the US HTS CODE column when it's there already"""
    with open("data/test/valid_us_hts_code.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert len(header) == csv_utilities.InventoryColumns.US_HTS_CODE.value + 1
        new_header = csv_utilities.create_header(header)
        assert len(new_header) == csv_utilities.InventoryColumns.US_HTS_CODE.value + 1
        assert csv_utilities.validate_header(header)
        assert csv_utilities.validate_header(new_header)

def test_valid_csv_with_us_hts_code():
    """ Test that a valid CSV with US HTS Code returns True """
    with open("data/test/valid_us_hts_code.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        row = next(reader)
        assert csv_utilities.validate_row(2, len(header), row, True, True, True)

def test_row_length_does_not_match_header():
    """ Test that a valid CSV row length different from header length returns False """
    with open("data/test/valid_us_hts_code.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        row = next(reader)
        assert not csv_utilities.validate_row(2, len(header) - 1, row, True, True, True)


# One real title per rule for products without an SKU, taken from the inventory export.
# Titles are passed as they appear in Shopify; the test lowercases them like create_row_with_codes.
TITLE_CASES = [
    ("Rats Get Fat T-Shirt Grey", HSCodes.COTTON_T_SHIRT),
    ("Trophy - Box Logo OD LS Tee Gun Black", HSCodes.COTTON_KNITTED_PULLOVER),
    ("Trophy - Machine Age Flannel Shirt Olive", HSCodes.COTTON_SHIRT_FLANNEL),
    ("Trophy - Coke Stripe Pants 11 Oz Natural", HSCodes.COTTON_TROUSERS),
    ("Trophy - Dirt Denim Coverall 14,5 Oz", HSCodes.COTTON_JACKET_BLUE_DENIM),
    ("Trophy - Watchman Cap Black", HSCodes.COTTON_HAT_KNITTED),
    ("Trophy - 15th Anniversary 1605 Jeans 14,5 Oz Standard Dirt Denim", HSCodes.JEANS_BLUE_DENIM),
    ("Trophy - 47 Civilian Trousers Khaki", HSCodes.COTTON_TROUSERS),
    ("PE-SKULL-POISON-RING-BLACK - Peanuts & Co SKULL POISON Ring - Silver/ Zirconia Black (Kopie)",
     HSCodes.SILVER_JEWELRY),
    ("HTC-EAGLE-BELT-BLK - Hollywood Trading Co. Eagle Belt w/ turquoise stones - Black",
     HSCodes.LEATHER_BELT),
    ("IH-XXX-DD - Double Duck Type I Jacket - Indigo", HSCodes.COTTON_JACKET_OTHER),
]


@pytest.mark.parametrize("title, expected", TITLE_CASES, ids=[case[0] for case in TITLE_CASES])
def test_get_hs_from_title(title, expected):
    """ Test that each product without an SKU gets the expected US HTS code from its title """
    assert csv_utilities.get_hs_from_title(title.lower()) == expected


@pytest.mark.parametrize("title", [
    # Only long-sleeved Trophy tees are pullovers
    "Trophy - Box Logo OD Tee Black",
    # Duck jackets only match the Iron Heart IH-XXX-DD sample
    "Dehen 1920 Duck Jacket - Brown",
    "Unknown Product",
])
def test_get_hs_from_title_no_match(title):
    """ Test that titles without a matching rule return None """
    assert csv_utilities.get_hs_from_title(title.lower()) is None
