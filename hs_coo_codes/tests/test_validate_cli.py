""" Test the CLI for the validate command """

from click.testing import CliRunner
from hs_coo_codes.validate_inventory import cli

def test_cli_exits_nonzero_for_invalid_csv():
    """ Test that the exit code is 1 when the CLI command fails """
    result = CliRunner().invoke(cli, ["data/test/empty.csv"])
    assert result.exit_code == 1

def test_cli_exits_zero_for_valid_csv():
    """ Test that the exit code is 0 when the CLI command succeeds """
    result = CliRunner().invoke(cli, ["data/test/valid.csv"])
    assert result.exit_code == 0