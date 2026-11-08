"""
Test the comparison of the inventory.
"""

import csv

from hs_coo_codes.compare_inventory import compare_inventory

def test_same_file_csv():
    """ Test that CSVs with same file name returns true in compare_inventory """
    assert compare_inventory("data/test/valid.csv", "data/test/valid.csv")

def test_identical_csv():
    """ Test that a identical CSVs returns true in compare_inventory """
    assert compare_inventory("data/test/valid.csv", "data/test/valid_identical.csv")

def test_no_hs_code_csv():
    """ Test that compare_inventory does not check HS Code """
    assert compare_inventory("data/test/valid.csv", "data/test/valid_no_hs_code.csv")

def test_no_coo_code_csv():
    """ Test that compare_inventory does not check COO CODE """
    assert compare_inventory("data/test/valid.csv", "data/test/valid_no_coo_code.csv")

def test_different_length_csv():
    """ Test that CSVs of different length return false """
    assert not compare_inventory("data/test/valid.csv", "data/test/valid_different_length.csv")
    assert not compare_inventory("data/test/valid_different_length.csv", "data/test/valid.csv")

def test_different_csv():
    """ Test that different CSVs return false """
    assert not compare_inventory("data/test/valid_different.csv", "data/test/valid.csv")

def test_short_row_csv():
    """ Test when a CSV row is too short """
    assert not compare_inventory("data/test/short_row.csv", "data/test/valid.csv")

def test_file_does_not_exist_csv():
    """ Test when a CSV does not exist """
    assert not compare_inventory("data/test/does_not_exist.csv", "data/test/valid.csv")

def test_file_no_hs_code_header_csv():
    """ Test a CSV file which does not have a HS Code in the header """
    assert not compare_inventory("data/test/no_hs_code_header.csv", "data/test/valid.csv")

def test_file_no_coo_code_header_csv():
    """ Test a CSV file which does not have a COO Code in the header """
    assert not compare_inventory("data/test/no_coo_code_header.csv", "data/test/valid.csv")

def test_file_us_hts_code_csv():
    """ Test a CSV file has a US HTS Code """
    assert compare_inventory("data/test/valid.csv", "data/test/valid_us_hts_code.csv")

def test_rejects_row_missing_us_hts_column(tmp_path):
    """Reject a 23-column row beneath a 24-column header."""
    with open(
        "data/test/valid_us_hts_code.csv",
        encoding="utf-8",
        newline="",
    ) as source:
        rows = list(csv.reader(source))

    # Keep the US HTS header, but remove its value from the first row.
    rows[1] = rows[1][:-1]

    malformed_file = tmp_path / "missing_us_hts_column.csv"
    with malformed_file.open(
        "w", encoding="utf-8", newline=""
    ) as output:
        csv.writer(output).writerows(rows)

    assert not compare_inventory(
        "data/test/valid.csv", malformed_file
    )
    assert not compare_inventory(
        malformed_file, "data/test/valid.csv"
    )
