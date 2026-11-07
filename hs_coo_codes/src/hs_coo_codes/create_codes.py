'''
Take a Shopify inventory export CSV as input.

Determine the Harmonized System (HS) and Country or Origin (COO) codes for each product.
Enter these codes in their respective columns.

Write the modified CSV to an output file.
'''

import csv
import logging
import os
from pathlib import Path
import sys
import tempfile

import click

from .validate_inventory import validate_inventory
from .compare_inventory import compare_inventory
from . import csv_utilities

@click.command()
@click.option('--input-file', required=True, type=click.Path(exists=True), help="Input CSV file.")
@click.option('--output-file', required=True, help="Output CSV file.")
def cli(input_file, output_file):
    """Main function"""

    if create_codes(input_file, output_file):
        logging.info("Code creation successful")
    else:
        logging.critical("Code creation failed")
        sys.exit(1)

def create_codes(input_file, output_file) -> bool:
    """Create HS and COO codes based upon info in input CSV"""
    # Reject identical paths
    if Path(input_file).resolve() == Path(output_file).resolve():
        logging.error("Input and output files identical: %s", input_file)
        return False

    # Validate input file
    if not validate_inventory(input_file, False, False):
        logging.error("Validation of input file %s failed", input_file)
        return False

    # Read the input CSV and write the output CSV
    output_path = Path(output_file)
    temporary_path = None

    try:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with (open(input_file, 'r', encoding='utf-8', newline="") as f_input,
              tempfile.NamedTemporaryFile(
                mode="w",
                encoding="utf-8",
                newline="",
                dir=output_path.parent,
                prefix=f".{output_path.name}.",
                suffix=".tmp",
                delete=False,
            ) as f_output
        ):
            temporary_path = Path(f_output.name)
            reader = csv.reader(f_input)
            writer = csv.writer(f_output)

            # Read and write the header
            writer.writerow(next(reader))

            # Parse each line of the input and add the HS and COO codes
            for row_number, row in enumerate(reader):
                new_row = csv_utilities.create_row_with_codes(row_number + 2, row)
                if new_row is None:
                    logging.error("Adding codes failed")
                    return False
                writer.writerow(new_row)

        # Validate output file
        if not validate_inventory(temporary_path, True, True):
            logging.error("Validation of output file %s failed", temporary_path)
            return False

        # Compare input and output files
        if not compare_inventory(input_file, temporary_path):
            logging.error("Comparison of input file (%s) and output file (%s) failed",
                          input_file, output_file)
            return False

        # Move the temporary file to the output file
        os.replace(temporary_path, output_path)

        return True

    except (OSError, csv.Error, StopIteration, FileNotFoundError) as e:
        logging.error("Code creation failed: %s", e)
        return False

    finally:
        # If the temporary file is moved it no longer exists.
        # On failure, remove the incomplete temporary file.
        if temporary_path is not None:
            temporary_path.unlink(missing_ok=True)


if __name__ == "__main__":
    cli.main()
