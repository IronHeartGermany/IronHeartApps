"""
COO Codes
"""

from enum import StrEnum

from .sku import StartSKU

class COOCodes(StrEnum):
    """Country of Origin Codes"""
    CHINA = "CN"
    GERMANY = "DE"
    JAPAN = "JP"
    GREAT_BRITAIN = "GB"
    SINGAPORE = "SG"
    USA = "US"

COO_CODES_CHINA = {StartSKU.BN3TH}

COO_CODES_GERMANY = {StartSKU.SACRED_DOG}

COO_CODES_GREAT_BRITAIN = {StartSKU.SIMMONS_BILT}

COO_CODES_JAPAN = {StartSKU.IH_BAGS,
                   StartSKU.IH_BELTS,
                   StartSKU.IH_BOTTOMS,
                   StartSKU.IH_BRASS,
                   StartSKU.IH_CAPS,
                   StartSKU.IH_GERMANY,
                   StartSKU.IH_JACKETS,
                   StartSKU.IH_MILITARY,
                   StartSKU.IH_PATCHES,
                   StartSKU.IH_PRINTED,
                   StartSKU.IH_SHIRTS,
                   StartSKU.IH_SWEATS,
                   StartSKU.IH_SIMMONS_BILT,
                   StartSKU.IH_SILVER,
                   StartSKU.IH_SNEAKERS,
                   StartSKU.IH_TEES_LONG_SLEEVE,
                   StartSKU.IH_TEES,
                   StartSKU.IH_THERMALS,
                   StartSKU.IH_VESTS,
                   StartSKU.IH_WOOL,
                   StartSKU.ASAHI,
                   StartSKU.CLUTCH,
                   StartSKU.MUSTANG,
                   StartSKU.PEANUTS,
                   StartSKU.PORTER,
                   StartSKU.RATS,
                   StartSKU.UTILITEES}

COO_CODES_SINGAPORE = {StartSKU.OBI}

COO_CODES_USA = {StartSKU.BEE_NATURAL,
                 StartSKU.BLACK_ROCK,
                 StartSKU.DEHEN,
                 StartSKU.GOOD_ART,
                 StartSKU.HOLLYWOOD_TRADING_CO,
                 StartSKU.RED_RABBIT,
                 StartSKU.WESCO,
                 StartSKU.WIGWAM}
