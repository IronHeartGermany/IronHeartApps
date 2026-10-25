"""
Test the validation of the CSV utilities.
"""

import csv

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

def test_missing_coo():
    """ Test that missing COO returns false when not ignored """
    with open("data/test/missing_coo.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        row = next(reader)
        assert not csv_utilities.validate_row(2, row, False, True)

def test_valid_csv():
    """ Test that a valid CSV returns True """
    with open("data/test/valid.csv", 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        row = next(reader)
        assert csv_utilities.validate_row(2, row, True, True)
