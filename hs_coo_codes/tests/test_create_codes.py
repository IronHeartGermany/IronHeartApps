"""
Test the creating codes.
"""

from hs_coo_codes.create_codes import create_codes

def test_valid_csv(tmp_path):
    """ Test that a valid CSV returns True """
    output_file = tmp_path / "output" / "valid_output.csv"
    assert create_codes("data/test/valid.csv", output_file)
    assert output_file.is_file()

def test_invalid_sku(tmp_path):
    """ Test that a CSV with an invalid SKU returns False """
    output_file = tmp_path / "output" / "invalid_output.csv"
    assert not create_codes("data/test/invalid_sku.csv", output_file)
