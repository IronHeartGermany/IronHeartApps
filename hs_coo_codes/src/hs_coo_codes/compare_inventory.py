'''
Compare a Shopify inventory CSV to another Shopify inventory CSV.

HS Codes and COO Codes are not compared.
'''

import csv
import itertools
import logging
import sys

import click

from .columns import InventoryColumns

logging.basicConfig(
    level=logging.INFO,
)

@click.command()
@click.option('--input-file-1',
              required=True,
              type=click.Path(exists=True),
              help="First Input CSV file.")
@click.option('--input-file-2',
              required=True,
              type=click.Path(exists=True),
              help="Second Input CSV file.")
def cli(input_file_1, input_file_2):
    """Main function"""

    if compare_inventory(input_file_1, input_file_2):
        logging.info("Compare successful")
    else:
        logging.critical("Compare failed")
        sys.exit(1)


def compare_inventory(input_file_1: str, input_file_2: str) -> bool:
    """ Compare the inventory CSV files """

    try:
        with (open(input_file_1, 'r', encoding='utf-8', newline="") as f_1,
              open(input_file_2, 'r', encoding='utf-8', newline="") as f_2):
            reader_1 = csv.reader(f_1)
            reader_2 = csv.reader(f_2)

            files_identical = True

            for index, (row_0, row_1) in enumerate(itertools.zip_longest(reader_1, reader_2),
                                                   start=1):

                # Check if files have different lengths
                if row_0 is None:
                    logging.error("%s is shorter than %s", input_file_1, input_file_2)
                    files_identical = False
                    break
                if row_1 is None:
                    logging.error("%s is shorter than %s", input_file_2, input_file_1)
                    files_identical = False
                    break

                # Check if the row from the first file has the correct length
                if len(row_0) != len(InventoryColumns) and len(row_0) != len(InventoryColumns) - 1:
                    logging.error("%s row_number=%d has length=%d but expected length %d or %d",
                                  input_file_1, index, len(row_0),
                                  len(InventoryColumns), len(InventoryColumns) - 1)
                    files_identical = False
                    break

                # Check if the row from the second file has the correct length
                if len(row_1) != len(InventoryColumns) and len(row_1) != len(InventoryColumns) - 1:
                    logging.error("%s row_number=%d has length=%d but expected length %d or %d",
                                  input_file_2, index, len(row_1),
                                  len(InventoryColumns), len(InventoryColumns) - 1)
                    files_identical = False
                    break

                # Compare each entry in each row for both files
                for column in InventoryColumns:
                    # Skip US HTS Code; skip HS Code and COO Code except in the header
                    if (column == InventoryColumns.US_HTS_CODE or
                        (index != 1 and column in (InventoryColumns.HS_CODE,
                                                   InventoryColumns.COO))):
                        continue

                    entry_0 = row_0[column.value]
                    entry_1 = row_1[column.value]
                    if entry_0 != entry_1:
                        logging.error("In row=%d column=%s: %s != %s",
                                      index, column.name, entry_0, entry_1)
                        files_identical = False

    except FileNotFoundError as e:
        logging.error("File could not be found: %s", e)
        return False
    except (OSError, UnicodeDecodeError, csv.Error) as e:
        logging.error("Comparison failed: %s", e)
        return False

    return files_identical


if __name__ == "__main__":
    cli.main()
