"""
Determine HS Codes for Iron Heart
"""

import logging

from .hs_codes import (HSCodes,
                       IH_COTTON_TROUSERS,
                       IH_JEANS,
                       IH_OVERALLS,
                       IH_SHORTS,
                       IH_WOOL_BLANKETS
)

from .sku import StartSKU

_IH_SKU_STARTS = {start for start in StartSKU if start.name.startswith("IH_")}


def get_hs_code_for_ih(sku: str, title: str) -> None | str:
    """Get the HS Code for Iron Heart"""
    for lookup in _IH_LOOKUPS:
        hs_code = lookup(sku, title)
        if hs_code is not None:
            return hs_code

    if sku.split("-", 1)[0] in _IH_SKU_STARTS:
        logging.error("Could not determine HS Code for Iron Heart for product (SKU=%s title=%s)",
                      sku, title)

    return None


def _get_hs_ih_bags(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Bags"""
    if sku.startswith(StartSKU.IH_BAGS + "-"):
        if any(word in title for word in ("denim duffle bag", "denim tote bag",
                                          "denim waist bag", "wabash waist bag",
                                          "whipcord waist bag",
                                          "denim and buttero leather holdall")):
            return HSCodes.COTTON_TOTE_BAG
        if any(word in title for word in ("leather waist bag",
                                          "leather diamond stitched shoulder bag")):
            return HSCodes.LEATHER_SLING_BAG

    return None


def _get_hs_ih_belts(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Belts"""
    if sku.startswith(StartSKU.IH_BELTS + "-"):
        if "leather" in title:
            return HSCodes.LEATHER_BELT

    return None


def _get_hs_ih_bottoms(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Bottoms """
    # Iron Heart Jeans
    if sku.startswith(IH_JEANS):
        # Super black, black fades to grey, black denim
        if "denim" in title and not any(word in title for word in ("black", "overdye", "white")):
            return HSCodes.JEANS_BLUE_DENIM
        return HSCodes.JEANS_BLACK_DENIM

    # Iron Heart Cotton Trousers
    if sku.startswith(IH_COTTON_TROUSERS):
        return HSCodes.COTTON_TROUSERS

    # Iron Heart Shorts
    if sku.startswith(IH_SHORTS):
        return HSCodes.COTTON_SHORTS

    # Iron Heart Overalls
    if sku.startswith(IH_OVERALLS):
        return HSCodes.COTTON_OVERALLS

    # Iron Heart Wool Blankets
    if sku.startswith(IH_WOOL_BLANKETS):
        return HSCodes.WOOL_BLANKET

    # Vests and jackets with format IH-XXXV and IH-XXXJ
    if sku.startswith("IH-"):
        if "vest" in title:
            return HSCodes.COTTON_VEST
        if any(word in title for word in ("jacket", "type iii")):
            if "denim" in title and not any(
                word in title for word in ("black", "overdye", "white")
            ):
                return HSCodes.COTTON_JACKET_BLUE_DENIM
            if any(word in title for word in ("super", "overdye", "duck",
                                              "whipcord", "black", "white")):
                return HSCodes.COTTON_JACKET_OTHER

    return None


def _get_hs_ih_brass(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Brass"""
    if sku.startswith(StartSKU.IH_BRASS + "-"):
        if "wallet chain" in title:
            return HSCodes.BRASS_CHAIN
        if any(word in title for word in ("key hook", "clip")):
            return HSCodes.BRASS_KEY_HOOK

    return None


def _get_hs_ih_caps(sku: str, _: str) -> None | str:
    """Get the US HTS Codes for IH Caps"""
    if sku.startswith(StartSKU.IH_CAPS + "-"):
        return HSCodes.WOOL_HAT_OTHER

    return None


def _get_hs_ih_germany(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Germany"""
    if sku.startswith(StartSKU.IH_GERMANY + "-"):
        if "cotton ribbed beanie" in title:
            return HSCodes.COTTON_HAT_KNITTED
        if "tote bag" in title:
            return HSCodes.COTTON_TOTE_BAG
        if "imabari towel" in title:
            return HSCodes.COTTON_TOWEL
        if "wool ribbed beanie" in title:
            return HSCodes.WOOL_HAT_KNITTED
        if "bandana" in title:
            return HSCodes.COTTON_BANDANA_HANDKERCHIEF
        if "mug" in title:
            return HSCodes.PORCELAIN_MUG
        if sku.startswith(("IHG-030", "IHG-029")):
            return HSCodes.COTTON_SOCKS
        if "leather keyring" in title:
            return HSCodes.LEATHER_ARTICLES
        if "denim keychain" in title:
            return HSCodes.OTHER_TEXTILES
        if any(word in title for word in ("keyring", "keychain")) and ("leather" not in title
                                                                       and "denim" not in title):
            return HSCodes.KEY_RING
        if any(word in title for word in ("cordovan card holder", "calf folding wallet",
                                          "trucker wallet", "cordovan wallet")):
            return HSCodes.LEATHER_WALLET
        if "apron" in title:
            return HSCodes.COTTON_APRON
        if "pouch" in title:
            return HSCodes.COTTON_POUCH
        if all(word in title for word in ("muffler", "primaloft")):
            return HSCodes.SYNTHETIC_MUFFLER

    return None


def _get_hs_ih_jackets(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Jackets"""
    if sku.startswith(StartSKU.IH_JACKETS + "-"):
        if any(word in title for word in ("denim", "wabash")):
            if any(word in title for word in ("black", "super", "overdye", "white")):
                return HSCodes.COTTON_JACKET_OTHER
            return HSCodes.COTTON_JACKET_BLUE_DENIM
        if any(word in title for word in ("whipcord", "herringbone", "moleskin",
                                          "chino", "duck", "hickory", "kersey",
                                          "canvas", "twill", "piqué", "paraffin",
                                          "oiled cotton", "reversible tanker",
                                          "serge", "ox riders")):
            return HSCodes.COTTON_JACKET_OTHER
        if "corduroy" in title:
            return HSCodes.COTTON_JACKET_CORDUROY
        if any(word in title for word in ("horsehide", "steer", "leather")):
            return HSCodes.LEATHER_JACKET
        if any(word in title for word in ("nylon", "cordura", "quilted rider",
                                          "street parka", "mountain parka")):
            return HSCodes.SYNTHETIC_JACKET

    return None


def _get_hs_ih_military(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Military"""
    if sku.startswith(StartSKU.IH_MILITARY + "-"):
        if "jacket" in title:
            if "denim" in title:
                return HSCodes.COTTON_JACKET_BLUE_DENIM
            if any(word in title for word in ("sateen",
                                              "oiled cotton",
                                              "whipcord",
                                              "serge",
                                              "duck")) or sku.startswith("IHM-41"):
                return HSCodes.COTTON_JACKET_OTHER
            if any(word in title for word in ("nylon",)):
                return HSCodes.SYNTHETIC_JACKET
            if any(word in title for word in ("wool",)):
                return HSCodes.WOOL_JACKET
        if "field coat" in title:
            return HSCodes.COTTON_JACKET_OTHER

    return None


def _get_hs_ih_printed(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Printed"""
    if sku.startswith(StartSKU.IH_PRINTED + "-"):
        if "t-shirt" in title:
            return HSCodes.COTTON_T_SHIRT

    return None


def _get_hs_ih_patches(sku: str, _: str) -> None | str:
    """Get the US HTS Codes for IH Patches"""
    if sku.startswith(StartSKU.IH_PATCHES + "-"):
        return HSCodes.WOVEN_PATCH_SYNTHETIC

    return None

def _get_hs_ih_shirts(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Shirts"""
    if sku.startswith(StartSKU.IH_SHIRTS + "-"):
        if any(word in title for word in ("uhf", "flannel", "check")) and "madras" not in title:
            return HSCodes.COTTON_SHIRT_FLANNEL
        if any(word in title for word in ("chambray", "summer shirt")):
            return HSCodes.COTTON_SHIRT_CHAMBRAY
        if "corduroy" in title:
            return HSCodes.COTTON_SHIRT_CORDUROY
        if "denim" in title:
            return HSCodes.COTTON_SHIRT_DENIM
        if any(word in title for word in ("madras", "double cloth", "ihsh-308-ind",
                                          "hickory", "wabash")):
            return HSCodes.COTTON_SHIRT_MULTI_COLOR
        if any(word in title for word in ("serge", "kersey", "whipcord",
                                          "satin", "dobby", "waffle", "fatigue", "twill",
                                          "moleskin", "oxford", "sateen", "ripstop", "duck",
                                          "sashiko", "johnny", "military", "gauze", "mechanic",
                                          "linen", "ihsh-410-blk", "ihsh-424-ind")):
            return HSCodes.COTTON_SHIRT_SINGLE_COLOR
        if "micro fleece" in title:
            return HSCodes.SYNTHETIC_SHIRT
        if "leather" in title:
            return HSCodes.LEATHER_SHIRT

    return None


def _get_hs_ih_silver(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Silver"""
    if sku.startswith(StartSKU.IH_SILVER + "-"):
        if any(word in title for word in ("ring", "pendant", "bangle", "chain")):
            return HSCodes.SILVER_JEWELRY

    return None


def _get_hs_ih_simmons_bilt(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Simmons Bilt"""
    if sku.startswith(StartSKU.IH_SIMMONS_BILT + "-"):
        if "jacket" in title:
            if "horsehide" in title:
                return HSCodes.LEATHER_JACKET
        if "shirt" in title:
            if any(word in title for word in ("horsehide", "deerskin")):
                return HSCodes.LEATHER_SHIRT

    return None


def _get_hs_ih_sneakers(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Sneakers"""
    if sku.startswith(StartSKU.IH_SNEAKERS + "-"):
        if "denim" in title:
            return HSCodes.NON_ATHLETIC_SNEAKERS

    return None


def _get_hs_ih_sweats(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Sweats"""
    if sku.startswith(StartSKU.IH_SWEATS + "-"):
        if any(word in title for word in ("hoodie", "crew neck sweat", "award sweater",
                                          "zip up sweater", "sweater jacket")):
            return HSCodes.COTTON_SWEATSHIRT
        if "sweat shorts" in title:
            return HSCodes.COTTON_SHORTS_KNITTED

    return None


def _get_hs_ih_tees(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Tees"""
    if sku.startswith(StartSKU.IH_TEES + "-"):
        if "t-shirt" in title and any(word in title for word in ("6.5oz", "7.5oz", "11oz")):
            return HSCodes.COTTON_T_SHIRT

    return None


def _get_hs_ih_tees_long_sleeve(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Tees Long Sleeve"""
    if sku.startswith(StartSKU.IH_TEES_LONG_SLEEVE + "-"):
        if "cotton" in title:
            return HSCodes.COTTON_KNITTED_PULLOVER

    return None


def _get_hs_ih_thermals(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Thermals"""
    if sku.startswith(StartSKU.IH_THERMALS + "-"):
        if any(word in title for word in ("waffle knit", "cotton knit", "11oz")):
            return HSCodes.COTTON_KNITTED_PULLOVER
        if all(word in title for word in ("loopwheel", "t-shirt")):
            return HSCodes.COTTON_T_SHIRT

    return None


def _get_hs_ih_vests(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Vests"""
    if sku.startswith(StartSKU.IH_VESTS + "-"):
        if any(word in title for word in ("dobby", "duck", "hickory", "whipcord")):
            return HSCodes.COTTON_VEST
        if "steerhide" in title:
            return HSCodes.LEATHER_SHIRT
        if "primaloft" in title:
            return HSCodes.SYNTHETIC_VEST_PADDED

    return None


def _get_hs_ih_wool(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Wool"""
    if sku.startswith(StartSKU.IH_WOOL + "-"):
        if "bush jacket" in title:
            return HSCodes.WOOL_JACKET

    return None


_IH_LOOKUPS = (
    _get_hs_ih_bags,
    _get_hs_ih_belts,
    _get_hs_ih_bottoms,
    _get_hs_ih_brass,
    _get_hs_ih_caps,
    _get_hs_ih_germany,
    _get_hs_ih_jackets,
    _get_hs_ih_military,
    _get_hs_ih_patches,
    _get_hs_ih_printed,
    _get_hs_ih_shirts,
    _get_hs_ih_silver,
    _get_hs_ih_simmons_bilt,
    _get_hs_ih_sneakers,
    _get_hs_ih_sweats,
    _get_hs_ih_tees,
    _get_hs_ih_tees_long_sleeve,
    _get_hs_ih_thermals,
    _get_hs_ih_vests,
    _get_hs_ih_wool,
)
