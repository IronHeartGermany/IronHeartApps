"""
Test the HS Codes for Non Iron Heart products.
"""

import logging

import pytest

from hs_coo_codes.hs_codes import HSCodes
from hs_coo_codes.hs_codes_for_non_ih import get_hs_code_for_non_ih


# One real (SKU, title) pair per branch, taken from the inventory export.
# Titles are passed as they appear in Shopify; the test lowercases them like create_row_with_codes.
NON_IH_CASES = [
    # Rats
    ("21-RTC-1103", "21-RTC-1103 - BIG LOGO HOODIE Black", HSCodes.COTTON_SWEATSHIRT),
    # Rats ombre check shirts are flannel
    ("21-RS-0905", "21-RS-0905 - Cotton Ombre Check Shirt brown", HSCodes.COTTON_SHIRT_FLANNEL),
    ("21-RTC-0802", "21-RTC-0801 - Circle Pocket L/S White", HSCodes.COTTON_KNITTED_PULLOVER),
    ("21-RA-0810", "21-RA-0810 - Line Socks \"The Rats\" White", HSCodes.COTTON_SOCKS),
    ("21-RA-1209", "21-RA-1209 - Rats Mug Black", HSCodes.PORCELAIN_MUG),
    ("21-RTC-1104", "21-RTC-1104 - SWEAT PANTS BLACK", HSCodes.COTTON_SWEATPANTS),
    ("21-RP-0911", "21-RP-0911 - Warm Up Pants Black", HSCodes.SYNTHETIC_WOVEN_TROUSERS),
    # Asahi
    ("AS-041-BEI", "AS-041-BEI - ASAHI Cotton Deck Shoes - Beige", HSCodes.NON_ATHLETIC_SNEAKERS),
    # Bee Natural: the title says "creme", not "cream"
    ("BEE-NATURAL", "BEE-NATURAL - Bee Natural - Mink Oil Creme", HSCodes.LEATHER_POLISH_OR_CREAM),
    # Black Rock
    ("BLACK-ROCK", "BLACK-ROCK - Black Rock Leather 'N' Rich", HSCodes.LEATHER_POLISH_OR_CREAM),
    # BN3TH
    ("BN3TH-M05020165-BLK", "BN3TH-M05020165-BLK - BN3TH AGUA VOLLEY 2N1 SWIM SHORT 5\"- BLACK",
     HSCodes.SYNTHETIC_SWIMSHORTS),
    ("BN3TH-M111024-BLK", "BN3TH-M111024-BLK - BN3TH CLASSIC BOXER BRIEF SOLID - BLACK",
     HSCodes.SYNTHETIC_UNDERWEAR),
    # Clutch
    ("CLUTCH-MENS-FILE", "CLUTCH-MENS-FILE - Clutch Magazine Vol. 96 / Men's File 30",
     HSCodes.CONSUMER_MAGAZINE),
    # Dehen
    ("DE-HDC01-GRY", "DE-HDC01-GRY - DEHEN 1920 Heavy Duty Crew Sweatshirt - Heather Grey",
     HSCodes.COTTON_SWEATSHIRT),
    ("DE-TS01-WHT", "DE-TS01-WHT - Dehen 1920 Heavy Duty T-Shirt - White", HSCodes.COTTON_T_SHIRT_WHITE),
    # The all-white T-shirt code excludes T-shirts with pockets
    ("DE-TS01P-WHT", "DE-TS01P-WHT - Dehen 1920 Heavy Duty Pocket T-Shirt - White",
     HSCodes.COTTON_T_SHIRT),
    ("DE-TS01-BLK", "DE-TS01-BLK - Dehen 1920 Heavy Duty T-Shirt - Black", HSCodes.COTTON_T_SHIRT),
    # Zip-up moto pieces are knitted wool, not T-shirts or woven shirts
    ("DE-SW0056-BLK-WHT", "DE-SW0056-BLK-WHT - Dehen 1920 1/4 Zip Moto-Jersey - Black / Off White",
     HSCodes.WOOL_SWEATER_FINE_KNIT),
    ("DE-WKC001-LOD", "DE-WKC001-LOD - Dehen 1920 Wool Knit Watch Cap - Loden", HSCodes.WOOL_HAT_KNITTED),
    ("DE-JA0002-BLK", "DE-JA0002-BLK - Dehen 1920 Varsity Jacket - Black", HSCodes.WOOL_JACKET),
    ("DE-N1-US-BLK", "DE-N1-US-BLK - Dehen 1920 Waxed Canvas N-1 Deck Jacket - Black",
     HSCodes.SHEEP_JACKET),
    ("DE-A-2E", "DE-A-2E - Deck Jacket 13.5oz Japanese Sateen Olive - Size Large",
     HSCodes.COTTON_JACKET_OTHER),
    # Waxed cotton does not count as water resistant
    ("DE-JA0029WC-OLV", "DE-JA0029WC-OLV - Flyer's Club Jacket Waxed Cotton Olive",
     HSCodes.COTTON_JACKET_OTHER),
    ("DE-JV0093-NAV", "DE-JV0093-NAV - Dehen 1920 Flight Vest Sateen - Navy", HSCodes.COTTON_VEST),
    ("DE-BC01-NAV", "DE-BC01-NAV - Dehen 1920 DKCo. Baseball Cap - Dark Navy", HSCodes.WOOL_HAT_OTHER),
    ("DE-BC02WC-SGE", "DE-BC02WC-SGE - DEHEN 1920 Dry Waxed Cotton Baseball Cap - Sage",
     HSCodes.COTTON_CAP),
    # Good Art
    ("GA-M25-RING-SI", "GA-M25-RING-SI - GOOD ART HLYWD Model 25 Ring - Sterling Silver",
     HSCodes.SILVER_JEWELRY),
    # "belt loop buddy" must be a tuple, not a string matched character by character
    ("GA-BLB-IH-BR", "GA-BLB-IH-BR - GOOD ART HLYWD x IRON HEART Belt Loop Buddy - Brass",
     HSCodes.BRASS_KEY_HOOK),
    ("GA-CUSTOM-ORDER", "GA-CUSTOM-ORDER - GOOD ART Custom Order", HSCodes.SILVER_JEWELRY),
    ("GA-LS-BLK", "GA-LS-BLK - GOOD ART HLYWD Heavyweight Long Sleeve T-Shirt - SAMPLE",
     HSCodes.COTTON_KNITTED_PULLOVER),
    ("GA-WALLET-BLK", "GA-WALLET-BLK - GOOD ART HLYWD Army Navy Wallet - Black", HSCodes.LEATHER_WALLET),
    ("GA-RUBBER-BRA", "GA-RUBBER-BRA - GOOD ART HLYWD Rubber Biscuit Rosette Bracelet",
     HSCodes.SILVER_JEWELRY),
    # Hollywood Trading Co
    ("HTC-STING-53-BELT-BLK", "HTC-STING-53-BELT-BLK - Hollywood Trading Co. \"Stingray 53\" Belt - Black",
     HSCodes.LEATHER_BELT),
    ("HTC-MED-WALLET-BLK",
     "HTC-MED-WALLET-BLK - Hollywood Trading Co. Medium Wallet w/ turquoise stones - Black",
     HSCodes.LEATHER_WALLET),
    ("HTC-WALLET-CHAIN-BLK", "HTC-WALLET-CHAIN-BLK - Hollywood Trading Co. Arrow Wallet Chain - Black",
     HSCodes.STEEL_CHAIN),
    ("HTC-KEY-FOB-BLK",
     "HTC-KEY-FOB-BLK - Hollywood Trading Co. Brass Key Fob w/ turquoise stones - Black",
     HSCodes.BRASS_KEY_HOOK),
    # Mustang
    ("MUSTANG-PA", "MUSTANG-PA -  \"Mustang Paste\" Natural Mustang Horse Leather Care",
     HSCodes.LEATHER_POLISH_OR_CREAM),
    ("MUSTANG-P-WAT", "MUSTANG-P-WAT -  \"Mustang P. Water\" Organic Mustang Horse Liquid Oil",
     HSCodes.PURE_HORSE_OIL),
    # Obbi Good Label
    ("OGL-BELT-RO-SPGAR-BLK", "OGL-BELT-RO-SPGAR-BLK - OGL Single Prong Leather Belt - Rough Out Black",
     HSCodes.LEATHER_BELT),
    ("OGL-WC-TYPE1", "OGL-WC-TYPE1 - Obbi Good Label Wallet Chain - Type 1", HSCodes.BRASS_CHAIN),
    # Peanuts
    ("PE-MR-SMILEY-T-SHIRT-WHT", "PE-MR-SMILEY-T-SHIRT-WHT - Peanuts & Co × GLADHAND & Co. Mr. SMILEY T-SHIRT - White",
     HSCodes.COTTON_T_SHIRT),
    ("PE-BOXER-SHORT-SPECIAL-NIGHTS-BLK",
     "PE-BOXER-SHORT-SPECIAL-NIGHTS-BLK - Peanuts & Co × GLADHAND & Co BOXER SHORTS \"SPECIAL NIGHTS!\" - Black",
     HSCodes.COTTON_WOVEN_BOXERS),
    ("PE-P-DECK-SHOES-BLK", "PE-P-DECK-SHOES-BLK - Peanuts & Co x ACVM WAXED COTTON P-DECK SHOES - Black",
     HSCodes.NON_ATHLETIC_SNEAKERS),
    ("PE-MR-SMILEY-BANDANA", "PE-MR-SMILEY-BANDANA - Peanuts & Co × GLADHAND & Co.- MR. SMILEY BANDANA",
     HSCodes.COTTON_BANDANA_HANDKERCHIEF),
    ("PE-NEWSPAPER-BAG-BLK",
     "PE-NEWSPAPER-BAG-BLK - Peanuts & Co x ACVM WAXED COTTON NEWSPAPER BAG - Black",
     HSCodes.COTTON_HANDBAG),
    ("PE-LONG-TRUCKER-WALLET-BLACK-LEATHER",
     "PE-LONG-TRUCKER-WALLET-BLACK-LEATHER - Peanuts & Co LONG TRUCKER WALLET- Black leather",
     HSCodes.LEATHER_WALLET),
    ("PE-THIN-BRACELET-SILVER", "PE-THIN-BRACELET-SILVER - Peanuts & Co PEANUTS THIN BRACELET - Silver",
     HSCodes.SILVER_JEWELRY),
    ("PE-PEANUTS-KEY-HOOK-BR", "PE-PEANUTS-KEY-HOOK-BR - Peanuts & Co Peanuts Key Hook - Brass",
     HSCodes.BRASS_KEY_HOOK),
    ("PE-LARGE-PEANUTS-PENDANT-BR",
     "PE-LARGE-PEANUTS-PENDANT-BR - Peanuts & Co LARGE PEANUTS PENDANT - Brass", HSCodes.BRASS_JEWELRY),
    ("PE-3PEANUTS-WALLET-CHAIN-BR",
     "PE-3PEANUTS-WALLET-CHAIN-BR - Peanuts & Co 3 PEANUTS WALLET CHAIN - Brass", HSCodes.BRASS_CHAIN),
    ("PE-CARABINER-BR", "PE-CARABINER-BR - Peanuts & Co PEANUTS CARABINER- Brass", HSCodes.BRASS_KEY_HOOK),
    ("PE-ZIPPO-BR", "PE-ZIPPO-BR - Peanuts & Co  - Peanuts ZIPPO - Brass", HSCodes.BRASS_LIGHTER),
    # Porter
    ("PO-FILM-ZIP-WALLET", "PO-FILM-ZIP-WALLET - Porter-Yoshida & Co. FILM ZIP WALLET - Black",
     HSCodes.LEATHER_WALLET),
    ("PO-CAPSULE-WALLET-BLK", "PO-CAPSULE-WALLET-BLK - Porter-Yoshida & Co. CAPSULE WALLET - Black",
     HSCodes.SYNTHETIC_WALLET),
    ("PO-COUNTER-BACKPACK-KHA",
     "PO-COUNTER-BACKPACK-KHA - Porter-Yoshida & Co. COUNTER SHADE BACKPACK - Woodland Khaki",
     HSCodes.SYNTHETIC_BACKPACK),
    ("PO-HEAT-MESSENGER-BLK", "PO-HEAT-MESSENGER-BLK - Porter-Yoshida & Co. HEAT MESSENGER BAG (L) - Black",
     HSCodes.SYNTHETIC_MESSENGER_OR_BRIEFCASE),
    ("PO-FORCE-SHOULDER-BAG-OLV",
     "PO-FORCE-SHOULDER-BAG-OLV - Porter-Yoshida & Co- FORCE SHOULDER BAG - Olive Drab",
     HSCodes.SYNTHETIC_HANDBAG),
    ("PO-TANKER-DUFFLE-BAG-BLU", "PO-TANKER-DUFFLE-BAG-BLU - Porter-Yoshida & Co. TANKER DUFFLE BAG - Blue",
     HSCodes.SYNTHETIC_TRAVEL_BAG),
    ("PO-COUNTER-DOCUMENT", "PO-COUNTER-DOCUMENT-KHA - Porter-Yoshida & Co. DOCUMENT CASE - Woodland Khaki",
     HSCodes.SYNTHETIC_DOCUMENT_CASE),
    # Red Rabbit only makes jewelry
    ("RR-BIKER-RING-SKULL", "RR-BIKER-RING-SKULL - Red Rabbit Biker Skull Ring", HSCodes.SILVER_JEWELRY),
    # Sacred Dog
    ("SD-BE-2", "SD-BE-2 - Sacred Dog Beanie", HSCodes.COTTON_HAT_KNITTED),
    ("SD-HO-1-01-BLK", "SD-HO-1-01-BLK – Sacred Dog Hoodie with chest print Black", HSCodes.COTTON_SWEATSHIRT),
    # Simmons Bilt
    ("SB-LEATHER-SHIRT-BLK", "SB-LEATHER-SHIRT-BLK - Simmons Bilt Leather Shirt Lambskin - Black",
     HSCodes.LEATHER_SHIRT),
    # A wool jacket must not be caught by the leather jacket rule
    ("SB-RA-WO-NAV", "SB-RA-WO-NAV - Simmons Bilt Wool Ranch Jacket - Navy", HSCodes.WOOL_JACKET),
    ("SB-D1-BRN", "SB-D1-BRN - Simmons Bilt D-1 Sheepskin Jacket - Brown", HSCodes.SHEEP_JACKET),
    ("SB-A2-HO-BRN", "SB-A2-HO-BRN - Simmons Bilt A-2 Blattwerk Horsehide Leather - Brown",
     HSCodes.LEATHER_JACKET),
    # Utilitees
    ("UTIL-NIN", "UTIL-NIN - UTILITEES 5.5oz Loopwheel Crew Neck T-Shirt - Natural Indigo",
     HSCodes.COTTON_T_SHIRT),
    # Wesco
    ("WE-BEE-SEAL-PLUS", "WE-BEE-SEAL-PLUS - Wesco Leather Boot Dressing Bee Seal Plus",
     HSCodes.LEATHER_POLISH_OR_CREAM),
    ("WE-BEE-OIL", "WE-BEE-OIL - Wesco Leather Boot Dressing Bee Oil", HSCodes.LEATHER_OIL),
    ("WE-LEATHER-LACES-63-BLK", "WE-LEATHER-LACES-63-BLK - WESCO Leather Laces - Black",
     HSCodes.LEATHER_SHOELACES),
    ("WE-NY-LACES63-TAN", "WE-NY-LACES63-TAN - WESCO Nylon Laces - Tan", HSCodes.OTHER_SHOELACES),
    ("WE-WAX-LACES-BRN", "WE-WAX-LACES-BRN - WESCO Waxed Laces - Brown", HSCodes.COTTON_SHOELACES),
    ("WE-103-BLK", "WE-103-BLK - Wesco Flexfit Cap Black", HSCodes.SYNTHETIC_CAP),
    ("WE-101-BLK-1", "WE-101-BLK-1 - Wesco 100th year Diamond Logo Hoodie Black", HSCodes.COTTON_SWEATSHIRT),
    ("WE-BT7710700-BLK", "WE-BT7710700-BLK - WESCO Custom Boss Engineer - Black",
     HSCodes.ENGINEER_BOOTS_WELT),
    ("WE-907-BRN", "WE-907-BRN - Wesco Custom Hendrik Chromexcel - Brown", HSCodes.WORK_BOOTS_WELT),
    # Wigwam: keywords must be tuples, not strings matched character by character
    ("WI-S1221-GRY", "WI-S1221-GRY - Wigwam At Work Crew 3-Pack Socks - Grey", HSCodes.COTTON_SOCKS),
    ("WI-S1349-WHT-GRY", "WI-S1349-WHT-GRY - Wigwam At Work DuraSole Pro 2-Pack Socks - White/Grey",
     HSCodes.SYNTHETIC_BLEND_SOCKS),
    ("WI-WORKMATE-GRY", "WI-WORKMATE-GRY - Wigwam Wool Workmate 2-Pack Socks Grey", HSCodes.WOOL_SOCKS),
    ("WI-F2322-BLK", "WI-F2322-BLK - Wigwam Merino Comfort Hiker 2-Pack - Black", HSCodes.WOOL_SOCKS),
]


@pytest.mark.parametrize("sku, title, expected", NON_IH_CASES, ids=[case[0] for case in NON_IH_CASES])
def test_get_hs_code_for_non_ih(sku, title, expected):
    """ Test that each Non Iron Heart product gets the expected US HTS code """
    assert get_hs_code_for_non_ih(sku, title.lower()) == expected


@pytest.mark.parametrize("sku, title", [
    ("WE-999-BLK", "WE-999-BLK - Wesco Gift Card"),
    ("PO-999-BLK", "PO-999-BLK - Porter-Yoshida & Co. Unknown Product"),
    ("IHT-1610-WHT", "IHT-1610-WHT - 6.5oz Loopwheel Crew Neck T-Shirt (Short)- White"),
])
def test_get_hs_code_for_non_ih_no_match(sku, title):
    """ Test that products without a matching Non Iron Heart rule return None """
    assert get_hs_code_for_non_ih(sku, title.lower()) is None


def test_get_hs_code_for_non_ih_logs_unknown_product(caplog):
    """ Test that an unknown product from a known Non Iron Heart brand is logged as an error """
    with caplog.at_level(logging.ERROR):
        get_hs_code_for_non_ih("WE-999-BLK", "we-999-blk - wesco gift card")
    assert "WE-999-BLK" in caplog.text


def test_get_hs_code_for_non_ih_does_not_log_ih_product(caplog):
    """ Test that Iron Heart products are left to the Iron Heart lookup without an error """
    with caplog.at_level(logging.ERROR):
        get_hs_code_for_non_ih("IHT-1610-WHT", "iht-1610-wht - 6.5oz loopwheel crew neck t-shirt")
    assert not caplog.records
