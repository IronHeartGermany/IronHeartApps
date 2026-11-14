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


def get_hs_code_for_ih(sku: str, title: str) -> None | str:
    """Get the HS Code for Iron Heart"""
    for lookup in _IH_LOOKUPS:
        hs_code = lookup(sku, title)
        if hs_code is not None:
            return hs_code

    #logging.error("Could not determine HS Code for Iron Heart for product with SKU=%s and title=%s",
    #              sku, title)
    return None

def _get_hs_ih_bottoms(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Bottoms """
    # Iron Heart Jeans
    if sku.startswith(IH_JEANS):
        # Super black, black fades to grey, black denim
        if sku.endswith(("SB", "BLK")):
            return HSCodes.JEANS_BLACK_DENIM
        return HSCodes.JEANS_BLUE_DENIM

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
        if "V" in sku and "vest" in title:
            return HSCodes.COTTON_VEST
        if "J" in sku:
            if "denim" in title and not ("black" in title or "overdye" in title):
                return HSCodes.COTTON_JACKET_BLUE_DENIM
            if "super" in title or "overdye" in title or "duck" in title:
                return HSCodes.COTTON_JACKET_OTHER

    return None

def _get_hs_ih_shirts(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Shirts"""
    if sku.startswith(StartSKU.IH_SHIRTS + "-"):
        if any(word in title for word in ("uhf", "flannel", "check")):
            return HSCodes.COTTON_SHIRT_FLANNEL
        if any(word in title for word in ("chambray", "summer shirt")):
            return HSCodes.COTTON_SHIRT_CHAMBRAY
        if "corduroy" in title:
            return HSCodes.COTTON_SHIRT_CORDUROY
        if "denim" in title:
            return HSCodes.COTTON_SHIRT_DENIM
        if any(word in title for word in ("madras", "double cloth", "ihsh-308-ind")):
            return HSCodes.COTTON_SHIRT_MULTI_COLOR
        if any(word in title for word in ("serge",  "hickory", "wabash", "kersey", "whipcord",
                                          "satin", "dobby", "waffle", "fatigue", "twill",
                                          "moleskin", "oxford", "sateen", "ripstop", "duck",
                                          "sashiko", "johnny", "military", "gauze", "mechanic",
                                          "linen", "ihsh-410-blk", "ihsh-424-ind")):
            return HSCodes.COTTON_SHIRT_SINGLE_COLOR
        if "corduroy" in title:
            return HSCodes.COTTON_SHIRT_CORDUROY
        if "micro fleece" in title:
            return HSCodes.SYNTHETIC_SHIRT
        if "leather" in title:
            return HSCodes.LEATHER_SHIRT

    return None


def _get_hs_ih_jackets(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Jackets"""
    if sku.startswith(StartSKU.IH_JACKETS + "-"):
        if any(word in title for word in ("denim", "wabash")):
            if any(word in title for word in ("black", "super", "overdye")):
                return HSCodes.COTTON_JACKET_OTHER
            return HSCodes.COTTON_JACKET_BLUE_DENIM
        if any(word in title for word in ("whipcord", "herringbone", "moleskin",
                                          "chino", "duck", "hickory", "kersey",
                                          "canvas", "twill", "piqué", "paraffin",
                                          "oiled cotton", "reversible tanker",
                                          "serge", "ox riders", "quilted rider")):
            return HSCodes.COTTON_JACKET_OTHER
        if "corduroy" in title:
            return HSCodes.COTTON_JACKET_CORDUROY
        if any(word in title for word in ("horsehide", "steer", "leather")):
            return HSCodes.LEATHER_JACKET
        if any(word in title for word in ("nylon", "cordura", "quilted rider",
                                          "street parka", "mountain parka")):
            return HSCodes.SYNTHETIC_JACKET

    return None

def _get_hs_ih_sweats(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Sweats"""
    if sku.startswith(StartSKU.IH_SWEATS + "-"):
        if any(word in title for word in ("hoodie", "crew neck sweat", "award sweater",
                                          "zip up sweater", "sweater jacket")):
            return HSCodes.COTTON_SWEATSHIRT
        if "sweat shorts" in title:
            return HSCodes.COTTON_SHORTS

    return None

def _get_hs_ih_military(sku: str, title: str) -> None | str:
    """Get the US HTS Codes for IH Military"""
    if sku.startswith(StartSKU.IH_MILITARY + "-"):
        if "jacket" in title:
            if any(word in title for word in ("sateen", "oiled cotton",
                                              "whipcord", "serge", "duck")):
                return HSCodes.COTTON_JACKET_OTHER
            if any(word in title for word in ("nylon")):
                return HSCodes.SYNTHETIC_JACKET
        if "field coat" in title:
            return HSCodes.COTTON_JACKET_OTHER

    return None


_IH_LOOKUPS = (
    _get_hs_ih_bottoms,
    _get_hs_ih_shirts,
    _get_hs_ih_jackets,
    _get_hs_ih_sweats,
    _get_hs_ih_military,
)