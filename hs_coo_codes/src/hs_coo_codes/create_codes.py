'''
Take a Shopify inventory export CSV as input.

Determine the Harmonized System (HS) and Country or Origin (COO) codes for each product.
Enter these codes in their respective columns.

Write the modified CSV to stdout.
'''

import csv
import logging
import sys

import click

from .validate_inventory import validate_inventory
from . import csv_utilities

@click.command()
@click.option('--input-file', required=True, type=click.Path(exists=True), help="Input CSV file.")
@click.option('--output-file', help="Output CSV file.")
def cli(input_file, output_file):
    """Main function"""

    if create_codes(input_file, output_file):
        logging.info("Code creation successful")
    else:
        logging.critical("Code creation failed")
        sys.exit(1)

def create_codes(input_file, output_file) -> bool:
    """Create HS and COO codes based upon info in input CSV"""
    print("----> ")
    # Validate input file
    if not validate_inventory(input_file, False, False):
        logging.error("Validation of input file %s failed", input_file)
        return False

    # Read the input CSV and write the output CSV
    try:
        with (open(input_file, 'r', encoding='utf-8') as f_input,
              open(output_file, 'w', encoding='utf-8') as f_output):
            reader = csv.reader(f_input)
            writer = csv.writer(f_output)

            # Read and write the header
            writer.writerow(next(reader))

            # Parse each line of the input and add the HS and COO codes
            for index, row in enumerate(reader):
                new_row = csv_utilities.create_row_with_codes(index + 2, row)
                if new_row is None:
                    logging.error("Adding codes failed")
                    return False
                writer.writerow(new_row)

    except FileNotFoundError as e:
        logging.error("Input file %s could not be found: %s", input_file, e)
        return False

    return True


if __name__ == "__main__":
    cli.main()
