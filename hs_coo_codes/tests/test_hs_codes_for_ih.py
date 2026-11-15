"""
Test the HS Codes for Iron Heart products.
"""

import pytest

from hs_coo_codes.hs_codes import HSCodes
from hs_coo_codes.hs_codes_for_ih import get_hs_code_for_ih


# One real (SKU, title) pair per branch, taken from the inventory export.
# Titles are passed as they appear in Shopify; the test lowercases them like create_row_with_codes.
IH_CASES = [
    # Bags
    ("IHE-37-IND", "IHE-37-IND - 21oz Denim Waist Bag - Indigo", HSCodes.COTTON_TOTE_BAG),
    ("IHE-45-BLK", "IHE-45-BLK - Diamond Stitched Leather Waist Bag - Black",
     HSCodes.LEATHER_WAIST_BAG),
    # A shoulder bag of messenger/satchel size is a "similar bag", not a handbag
    ("IHE-40-BLK", "IHE-40-BLK - Rectangular Leather Diamond Stitched Shoulder Bag Black",
     HSCodes.LEATHER_SLING_BAG),
    # Belts
    ("IHB-10-BLK", "IHB-10-BLK - Heavy Duty \"Tochigi\" Leather Belt - Black", HSCodes.LEATHER_BELT),
    # Bottoms
    ("IH-555S-SBG", "IH-555S-SBG - 21oz Selvedge Denim Slim Cut Jeans - Superblack (Fades To Grey)",
     HSCodes.JEANS_BLACK_DENIM),
    ("IH-720-IVO", "IH-720-IVO - Whipcord Chino Pants Ivory", HSCodes.COTTON_TROUSERS),
    ("IH-725-KHA", "IH-725-KHA - 11oz West Point Chino Shorts - Khaki", HSCodes.COTTON_SHORTS),
    ("IH-805-IND", "IH-805-IND - 21oz Selvedge Denim Double Knee Overalls - Indigo",
     HSCodes.COTTON_OVERALLS),
    ("IH-X-IF-01", "IH-X-IF-01 - Iron Heart x Indigofera Friendship Blanket", HSCodes.WOOL_BLANKET),
    ("IH-634S-142OD", "IH-634S-142OD - 14oz Selvedge Denim Straight Cut Jeans - Indigo Overdyed Black",
     HSCodes.JEANS_BLACK_DENIM),
    # IH-526 is a jacket model, not whipcord trousers (bug 2)
    ("IH-526-ODG", "IH-526-ODG - 12oz Whipcord Type III Jacket - Olive Drab Green",
     HSCodes.COTTON_JACKET_OTHER),
    ("IH-526J-142IB", "IH-526J-142IB - 14oz Selvedge Denim Modified Type III Jacket - Indigo/Black",
     HSCodes.COTTON_JACKET_OTHER),
    ("IH-526SVOD", "IH-526SVOD - 21oz Selvedge Denim Modified Type III Vest Overdyed Black",
     HSCodes.COTTON_VEST),
    ("IH-101J-SR", "IH-101J-SR - 18oz Selvedge Denim Storm Rider Jacket - Indigo",
     HSCodes.COTTON_JACKET_BLUE_DENIM),
    # Brass
    ("BRASS-W6", "BRASS-W6 - Wallet Chain with Hook and Rings - Brass", HSCodes.BRASS_CHAIN),
    ("BRASS-W10", "BRASS-W10 - Key Hook with Rings - Brass", HSCodes.BRASS_KEY_HOOK),
    # Caps
    ("IHC-18-SKR", "IHC-18-SKR - Iron Heart 'Skull Rider' Snapback Cap Black", HSCodes.WOOL_HAT_OTHER),
    # Iron Heart Germany
    ("IHG-081-GRY", "IHG-081-GRY - Cotton Ribbed Beanie - Grey", HSCodes.COTTON_HAT_KNITTED),
    ("IHG-065-ORA-BLK", "IHG-065-ORA-BLK - Iron Heart Small Imabari Towel - Orange/Black",
     HSCodes.COTTON_TOWEL),
    ("IHG-030-3-WHT", "IHG-030-3-WHT - 3-Pack Iron Heart Boot Socks - White", HSCodes.COTTON_SOCKS),
    ("IHG-067-BLK", "IHG-067-BLK - Buttero Leather Keyring - Black", HSCodes.LEATHER_ARTICLES),
    # Denim strap with chrome hardware is a textile article, not brass
    ("IHG-115", "IHG-115 - 21oz Denim Keychain", HSCodes.OTHER_TEXTILES),
    ("IHG-056-IND", "IHG-056-IND - 21oz Selvedge Denim Apron - Indigo", HSCodes.COTTON_APRON),
    ("IHG-092", "IHG-092 - 21oz Selvedge Denim Zip-Up Pouch", HSCodes.COTTON_POUCH),
    ("IHG-097-BLK", "IHG-097-BLK - PrimaLoft® Muffler - Black", HSCodes.SYNTHETIC_MUFFLER),
    # Jackets
    ("IHJ-139-IND", "IHJ-139-IND - 19oz Selvedge Denim Type II Jacket - Indigo",
     HSCodes.COTTON_JACKET_BLUE_DENIM),
    ("IHJ-69-KHA", "IHJ-69-KHA - Corduroy Modified Type III Jacket - Khaki",
     HSCodes.COTTON_JACKET_CORDUROY),
    ("IHJ-128-BLK", "IHJ-128-BLK - Japanese Horsehide Double Motorcycle Jacket - Black",
     HSCodes.LEATHER_JACKET),
    ("IHJ-131-BLK", "IHJ-131-BLK - CORDURA® Windbreaker - Black", HSCodes.SYNTHETIC_JACKET),
    # Military: "nylon" must not match any title containing an "n" (bug 1)
    ("IHM-27-OLV", "IHM-27-OLV - Sateen M65 Field Jacket - Olive", HSCodes.COTTON_JACKET_OTHER),
    ("IHM-42-IND", "IHM-42-IND - 16oz Natural Indigo Selvedge Denim M65 Field Jacket",
     HSCodes.COTTON_JACKET_BLUE_DENIM),
    ("IHM-43-NAV", "IHM-43-NAV - Nylon Type L-2B Flight Jacket - Navy Blue", HSCodes.SYNTHETIC_JACKET),
    ("IHM-49-BLK", "IHM-49-BLK - 21oz Melton Wool M65 Field Jacket - Black", HSCodes.WOOL_JACKET),
    # Patches
    ("IHP-JAPAN", "IHP-JAPAN - Iron Heart Japan Woven Patches", HSCodes.WOVEN_PATCH_SYNTHETIC),
    # Printed
    ("IHPT-2302-WHT", "IHPT-2302-WHT - 7.5oz Printed Loopwheel Crew Neck T-Shirt - White",
     HSCodes.COTTON_T_SHIRT),
    # Shirts: madras is not napped flannel (bug 5)
    ("IHSH-355-RED", "IHSH-355-RED - 5oz Selvedge Madras Check Western Shirt - Red",
     HSCodes.COTTON_SHIRT_MULTI_COLOR),
    ("IHSH-232-RED", "IHSH-232-RED - Ultra Heavy Flannel Buffalo Check Western Shirt - Red/Black",
     HSCodes.COTTON_SHIRT_FLANNEL),
    ("IHSH-21-BLU", "IHSH-21-BLU - 10oz Selvedge Chambray Work Shirt", HSCodes.COTTON_SHIRT_CHAMBRAY),
    ("IHSH-398-CAM", "IHSH-398-CAM - 11oz Corduroy Western Shirt - Camel",
     HSCodes.COTTON_SHIRT_CORDUROY),
    ("IHSH-292-IND", "IHSH-292-IND - 18oz Vintage Selvedge Denim CPO Shirt - Indigo",
     HSCodes.COTTON_SHIRT_DENIM),
    ("IHSH-216-NAV", "IHSH-216-NAV - Heavy Moleskin CPO Shirt - Navy",
     HSCodes.COTTON_SHIRT_SINGLE_COLOR),
    ("IHSH-464-WHT", "IHSH-464-WHT - FW26 - Leather Western Shirt - White", HSCodes.LEATHER_SHIRT),
    # Silver
    ("IHSI-16", "IHSI-16 - Iron Heart Sterling Silver Button Ring", HSCodes.SILVER_JEWELRY),
    # Simmons Bilt
    ("IHSB-PR-NAT",
     "IHSB-PR-NAT - Iron Heart X Simmons Bilt Horsehide Western Shirt - The Pale Rider - Natural",
     HSCodes.LEATHER_SHIRT),
    # Sneakers
    ("IHSN-01-BLK", "IHSN-01-BLK - 21oz Denim Low-Top Sneakers Superblack",
     HSCodes.NON_ATHLETIC_SNEAKERS),
    # Sweats: sweat shorts are knitted, not woven (bug 6)
    ("IHSW-10-BLK", "IHSW-10-BLK - 14oz Ultra Heavyweight Cotton Zip Up Hoodie Black",
     HSCodes.COTTON_SWEATSHIRT),
    ("IHSW-50-BLK", "IHSW-50-BLK - Ultra Heavy Cotton Fleece Printed Sweat Shorts – Black",
     HSCodes.COTTON_SHORTS_KNITTED),
    # Tees
    ("IHT-1610-WHT", "IHT-1610-WHT - 6.5oz Loopwheel Crew Neck T-Shirt (Short)- White",
     HSCodes.COTTON_T_SHIRT),
    ("IHT-1600-CRM", "IHT-1600-CRM - 11oz Crew Neck T-Shirt - Cream", HSCodes.COTTON_T_SHIRT),
    # Tees long sleeve
    ("IHTB-12-WHT", "IHTB-12-WHT - 11oz Cotton Knit Long-Sleeved Sweater - White Body with Stripes",
     HSCodes.COTTON_KNITTED_PULLOVER),
    # Thermals
    ("IHTL-1301-IND", "IHTL-1301-IND - Waffle Knit Thermal Long Sleeved Crew Neck - Indigo",
     HSCodes.COTTON_KNITTED_PULLOVER),
    # Vests
    ("IHV-03-BRN", "IHV-03-BRN - 17oz Cotton Duck Work Vest - Brown", HSCodes.COTTON_VEST),
    ("IHV-45-BLK", "IHV-45-BLK - Japanese Steerhide Modified Type III Vest - Black",
     HSCodes.LEATHER_SHIRT),
    # Wool
    ("IHW-20-RED", "IHW-20-RED - Wool Buffalo Check Bush Jacket - Red", HSCodes.WOOL_JACKET),
]


@pytest.mark.parametrize("sku, title, expected", IH_CASES, ids=[case[0] for case in IH_CASES])
def test_get_hs_code_for_ih(sku, title, expected):
    """ Test that each Iron Heart product gets the expected US HTS code """
    assert get_hs_code_for_ih(sku, title.lower()) == expected


@pytest.mark.parametrize("sku, title", [
    ("DE-TS01-SPR", "DE-TS01-SPR - Heavy Duty T-Shirt - Spruce"),
    ("IHG-999", "IHG-999 - Unknown Iron Heart Germany Product"),
])
def test_get_hs_code_for_ih_no_match(sku, title):
    """ Test that products without a matching Iron Heart rule return None """
    assert get_hs_code_for_ih(sku, title.lower()) is None


def test_hs_codes_are_ten_digits():
    """ Test that every US HTS code is exactly 10 digits, without dots """
    for code in HSCodes:
        assert code.isdigit() and len(code) == 10, f"{code.name} = {code.value}"
