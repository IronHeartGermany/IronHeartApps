""" Test the CLI for the validate command """

from click.testing import CliRunner
from hs_coo_codes.validate_inventory import cli
from hs_coo_codes.create_codes import create_codes

def test_cli_exits_nonzero_for_invalid_csv():
    """ Test that the exit code is 1 when the CLI command fails """
    result = CliRunner().invoke(cli, ["--input-file=data/test/empty.csv"])
    assert result.exit_code == 1

def test_cli_exits_zero_for_valid_csv():
    """ Test that the exit code is 0 when the CLI command succeeds """
    result = CliRunner().invoke(cli, ["--input-file=data/test/valid.csv"])
    assert result.exit_code == 0

def test_cli_check_us_hts_passes_for_output_csv(tmp_path):
    """ Test that an output CSV with US HTS codes passes all checks """
    output_file = tmp_path / "output.csv"
    assert create_codes("data/test/valid.csv", output_file)

    result = CliRunner().invoke(cli, [f"--input-file={output_file}",
                                      "--check-hs", "--check-coo", "--check-us-hts"])
    assert result.exit_code == 0

def test_cli_check_us_hts_fails_for_shopify_csv():
    """ Test that a Shopify export without the US HTS column fails the US HTS check """
    result = CliRunner().invoke(cli, ["--input-file=data/test/valid.csv", "--check-us-hts"])
    assert result.exit_code == 1

def test_cli_check_us_hts_fails_for_empty_us_hts(tmp_path):
    """ Test that an output CSV with an empty US HTS code fails the US HTS check """
    output_file = tmp_path / "output.csv"
    assert create_codes("data/test/valid.csv", output_file)

    # Blank out the US HTS value (last column) in the data rows
    lines = output_file.read_text(encoding="utf-8").splitlines()
    lines[1:] = [line.rsplit(",", 1)[0] + "," for line in lines[1:]]
    output_file.write_text("\n".join(lines), encoding="utf-8")

    result = CliRunner().invoke(cli, [f"--input-file={output_file}", "--check-us-hts"])
    assert result.exit_code == 1
