'''
Validate a Shopify inventory CSV.

Depending on the command line options, validation can be performed with
and without expecting the HS and COO codes.
'''

import csv
import logging
import sys

import click

from . import csv_utilities

logging.basicConfig(
    level=logging.INFO,
)

@click.command()
@click.option('--input-file', required=True, type=click.Path(exists=True), help="Input CSV file.")
@click.option('--check-hs', is_flag=True, help="Check for existence of HS Code in CSV.")
@click.option('--check-coo', is_flag=True, help="Check for existence of COO Code in CSV.")
def cli(input_file, check_hs, check_coo):
    """Main function"""

    if validate_inventory(input_file, check_hs, check_coo):
        logging.info("Validation successful")
    else:
        logging.critical("Validation failed")
        sys.exit(1)


def validate_inventory(input_file: str, check_hs: bool, check_coo: bool) -> bool:
    """ Validate the inventory CSV """
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)

            # Get header.  An exception indicates it's empty.
            try:
                header = next(reader)
            except StopIteration as e:
                logging.error("Error getting header: %s", e)
                return False

            # Validate header
            if not csv_utilities.validate_header(header):
                logging.error("Header validation failed")
                return False

            # Validate rows after header
            for index, row in enumerate(reader):
                row_number = index + 2
                if not csv_utilities.validate_row(row_number, row, check_hs, check_coo):
                    logging.error("Row validation failed")
                    return False

    except FileNotFoundError as e:
        logging.error("File %s could not be found: %s", input_file, e)
        return False

    return True


if __name__ == "__main__":
    cli.main()
