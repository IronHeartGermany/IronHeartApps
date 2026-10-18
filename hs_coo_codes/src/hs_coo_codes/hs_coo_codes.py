'''
Take a Shopify inventory export CSV as input.

Determine the Harmonized System (HS) and Country or Origin (COO) codes for each product.
Enter these codes in their respective columns.

Write the modified CSV to stdout.
'''

import click

@click.command()
@click.argument('input_file', type=click.Path(exists=True))
def cli(input_file):
    ''' Main function '''

    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
        print(content)

if __name__ == "__main__":
    cli.main()
