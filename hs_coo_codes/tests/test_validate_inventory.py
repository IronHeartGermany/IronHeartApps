"""
Test the validation of the inventory.
"""

from hs_coo_codes import validate_inventory

def test_empty_csv():
    """ Test that an empty CSV returns false in validate_inventory """
    assert not validate_inventory.validate_inventory("data/test/empty.csv", False, False)

def test_short_header():
    """ Test that a CSV with a short header returns false in validate_inventory """
    assert not validate_inventory.validate_inventory("data/test/short_header.csv", False, False)

def test_bad_header_csv():
    """ Test that a CSV with a bad header returns false in validate_inventory """
    assert not validate_inventory.validate_inventory("data/test/bad_header.csv", False, False)

def test_empty_row_element_csv():
    """ Test that a CSV with an empty row element returns false in validate_inventory """
    assert not validate_inventory.validate_inventory("data/test/empty_row_element.csv", False, False)

def test_row_too_short_csv():
    """ Test that a CSV with a short row returns false in validate_inventory """
    assert not validate_inventory.validate_inventory("data/test/short_row.csv", False, False)

def test_missing_hs_code():
    """ Test that missing HS Codes returns false when not ignored """
    assert not validate_inventory.validate_inventory("data/test/missing_hs_code.csv", True, False)

def test_missing_coo():
    """ Test that missing COO returns false when not ignored """
    assert not validate_inventory.validate_inventory("data/test/missing_coo.csv", False, True)

def test_valid_csv():
    """ Test that a valid CSV returns True """
    assert validate_inventory.validate_inventory("data/test/valid.csv", True, True)

