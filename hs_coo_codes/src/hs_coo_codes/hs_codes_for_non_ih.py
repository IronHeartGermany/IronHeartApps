"""
Determine HS Codes for Non Iron Heart
"""

import logging

from .hs_codes import HSCodes

from .sku import StartSKU

_NON_IH_SKU_STARTS = {start for start in StartSKU if not start.name.startswith("IH_")}

def get_hs_code_for_non_ih(sku: str, title: str) -> None | str:
    """Get the HS Code for Non Iron Heart"""
    for lookup in _NON_IH_LOOKUPS:
        hs_code = lookup(sku, title)
        if hs_code is not None:
            return hs_code

#    if sku.split("-", 1)[0] in _NON_IH_SKU_STARTS:
#        logging.error("Could not determine HS Code for Non Iron Heart for product (SKU=%s title=%s)",
#                      sku, title)

    return None


def _get_hs_code_for_bn3th(sku: str, title: str):
    """Get the US HTS Codes for Bn3th"""
    if sku.startswith(StartSKU.BN3TH + "-"):
        if "boxer brief" in title:
            return HSCodes.SYNTHETIC_UNDERWEAR
        if "swim short" in title:
            return HSCodes.SYNTHETIC_SWIMSHORTS

    return None


def _get_hs_code_for_sacred_dog(sku: str, title: str):
    """Get the US HTS Codes for Sacred Dog"""
    if sku.startswith(StartSKU.SACRED_DOG + "-"):
        if "beanie" in title:
            return HSCodes.COTTON_HAT_KNITTED
        if "hoodie" in title:
            return HSCodes.COTTON_SWEATSHIRT

    return None


def _get_hs_code_for_simmons_bilt(sku: str, title: str):
    """Get the US HTS Codes for Simmons Bilt"""
    if sku.startswith(StartSKU.SIMMONS_BILT + "-"):
        if "shirt" in title:
            return HSCodes.LEATHER_SHIRT
        if any(word in title for word in ("jacket", "horsehide")):
            return HSCodes.LEATHER_JACKET

    return None


def _get_hs_code_for_obi(sku: str, title: str):
    """Get the US HTS Codes for Obi"""
    if sku.startswith(StartSKU.OBI + "-"):
        if "leather belt" in title:
            return HSCodes.LEATHER_BELT
        if "wallet chain" in title:
            return HSCodes.BRASS_CHAIN

    return None


def _get_hs_code_for_asahi(sku: str, title: str):
    """Get the US HTS Codes for Asahi"""
    if sku.startswith(StartSKU.ASAHI + "-"):
        if any(word in title for word in ("cotton deck", "cotton canvas", "cotton slip on")):
            return HSCodes.NON_ATHLETIC_SNEAKERS

    return None


def _get_hs_code_for_clutch(sku: str, title: str):
    """Get the US HTS Codes for Clutch"""
    if sku.startswith(StartSKU.CLUTCH + "-"):
        if "magazine" in title:
            return HSCodes.CONSUMER_MAGAZINE

    return None


def _get_hs_code_for_mustang(sku: str, title: str):
    """Get the US HTS Codes for Mustang"""
    if sku.startswith(StartSKU.MUSTANG + "-"):
        if "leather care" in title:
            return HSCodes.LEATHER_POLISH_OR_CREAM
        if "horse liquid oil" in title:
            return HSCodes.PURE_HORSE_OIL
        print("------> ", sku, title)

    return None


_NON_IH_LOOKUPS = (
    _get_hs_code_for_bn3th,
    _get_hs_code_for_sacred_dog,
    _get_hs_code_for_simmons_bilt,
    _get_hs_code_for_obi,
    _get_hs_code_for_asahi,
    _get_hs_code_for_clutch,
    _get_hs_code_for_mustang,
)