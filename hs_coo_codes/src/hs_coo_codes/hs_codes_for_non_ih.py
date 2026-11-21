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

    if sku.split("-", 1)[0] in _NON_IH_SKU_STARTS:
        logging.error("Could not determine HS Code for Non Iron Heart for product (SKU=%s title=%s)",
                      sku, title)

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

    return None


def _get_hs_code_for_peanuts(sku: str, title: str):
    """Get the US HTS Codes for Peanuts"""
    if sku.startswith(StartSKU.PEANUTS + "-"):
        if "t-shirt" in title:
            return HSCodes.COTTON_T_SHIRT
        if "boxer shorts" in title:
            return HSCodes.COTTON_WOVEN_BOXERS
        if all(word in title for word in ("cotton", "shoes")):
            return HSCodes.NON_ATHLETIC_SNEAKERS
        if "bandana" in title:
            return HSCodes.COTTON_BANDANA_HANDKERCHIEF
        if all(word in title for word in ("cotton", "newspaper", "bag")):
            return HSCodes.COTTON_HANDBAG
        if all(word in title for word in ("trucker", "wallet", "leather")):
            return HSCodes.LEATHER_WALLET
        if "silver" in title:
            return HSCodes.SILVER_JEWELRY
        if "brass" in title:
            if "key" in title and any(word in title for word in ("chain", "hook",
                                                                 "ring", "holder")):
                return HSCodes.BRASS_KEY_HOOK
            if "pendant" in title:
                return HSCodes.BRASS_JEWELRY
            if "wallet chain" in title:
                return HSCodes.BRASS_CHAIN
            if "carabiner" in title:
                return HSCodes.BRASS_KEY_HOOK
            if "zippo" in title:
                return HSCodes.BRASS_LIGHTER

    return None

def _get_hs_code_for_porter(sku: str, title: str):
    """Get the US HTS Codes for Porter"""
    if sku.startswith(StartSKU.PORTER + "-"):
        if any(word in title for word in ("counter zip wallet", "film zip wallet",
                                          "leather zip wallet", "film coin & card case",
                                          "glaze zip coin case")):
            return HSCodes.LEATHER_WALLET
        if any(word in title for word in ("heat wallet", "capsule wallet",
                                          "counter shade wallet", "hybrid wallet",
                                          "camouflage wallet card case")):
            return HSCodes.SYNTHETIC_WALLET
        if any(word in title for word in("counter shade backpack", "explorer daypack",
                                         "force daypack")):
            return HSCodes.SYNTHETIC_BACKPACK
        if any(word in title for word in("monochrome messenger", "hybrid 2way briefcase"
                                         "heat messenger bag", "force 3way briefcase",
                                         "heat 2way briefcase", "tanker 2way briefcase",
                                         "force 3way briefcase", "heat messenger bag",
                                         "hybrid 2way briefcase")):
            return HSCodes.SYNTHETIC_MESSENGER_OR_BRIEFCASE
        if any(word in title for word in ("force shoulder bag", "force shoulder pouch",
                                          "tanker shoulder bag", "counter shade shoulder bag",
                                          "hybrid sling shoulder bag", "tanker travel case")):
            return HSCodes.SYNTHETIC_HANDBAG
        if any(word in title for word in ("force 2way tote bag", "flex 2way tote bag",
                                          "3way duffle bag", "2way duffle bag",
                                          "tanker duffle bag", "flex 2way helmet bag",
                                          "counter shade helmet bag", "force 2 way helmet bag",
                                          "heat waist bag", "force 2way waist bag")):
            return HSCodes.SYNTHETIC_TRAVEL_BAG
        if any(word in title for word in ("document case",)):
            return HSCodes.SYNTHETIC_DOCUMENT_CASE
        if any(word in title for word in ("coppi sacoche",)):
            return HSCodes.COTTON_HANDBAG

    return None


def _get_hs_code_for_rats(sku: str, title: str):
    """Get the US HTS Codes for Rats"""
    if sku.startswith(StartSKU.RATS + "-"):
        if "mug" in title:
            return HSCodes.PORCELAIN_MUG
        if any(word in title for word in ("hoodie", "crew neck sweat")):
            return HSCodes.COTTON_SWEATSHIRT
        if any(word in title for word in ("flannel", "ombre")):
            return HSCodes.COTTON_SHIRT_FLANNEL
        if any(word in title for word in ("script", "circle pocket l/s")):
            return HSCodes.COTTON_KNITTED_PULLOVER
        if any(word in title for word in ("line socks",)):
            return HSCodes.COTTON_SOCKS
        if any(word in title for word in ("sweat pants",)):
            return HSCodes.COTTON_SWEATPANTS
        if any(word in title for word in ("warm up pants",)):
            return HSCodes.SYNTHETIC_WOVEN_TROUSERS

    return None


def _get_hs_code_for_utilitees(sku: str, title: str):
    """Get the US HTS Codes for Utilitees"""
    if sku.startswith(StartSKU.UTILITEES + "-"):
        if "crew neck t-shirt" in title:
            return HSCodes.COTTON_T_SHIRT

    return None


def _get_hs_code_for_bee_natural(sku: str, title: str):
    """Get the US HTS Codes for Bee Natural"""
    if sku.startswith(StartSKU.BEE_NATURAL + "-"):
        if "mink oil cream" in title:
            return HSCodes.LEATHER_POLISH_OR_CREAM

    return None


def _get_hs_code_for_black_rock(sku: str, title: str):
    """Get the US HTS Codes for Black Rock"""
    if sku.startswith(StartSKU.BLACK_ROCK + "-"):
        if "leather 'n' rich" in title:
            return HSCodes.LEATHER_POLISH_OR_CREAM

    return None


def _get_hs_code_for_dehen(sku: str, title: str):
    """Get the US HTS Codes for Dehen"""
    if sku.startswith(StartSKU.DEHEN+ "-"):
        if any(word in title for word in ("crew sweatshirt", "heavy duty hoodie")):
            return HSCodes.COTTON_SWEATSHIRT
        if any(word in title for word in ("t-shirt",)):
            if "white" in title:
                return HSCodes.COTTON_T_SHIRT_WHITE
            return HSCodes.COTTON_T_SHIRT
        if any(word in title for word in ("moto-hoodie", "moto-jersey", "moto-sweater")):
            return HSCodes.COTTON_T_SHIRT
        if any(word in title for word in ("wool knit watch cap",)):
            return HSCodes.WOOL_HAT_KNITTED
        if any(word in title for word in ("varsity jacket",)):
            return HSCodes.WOOL_JACKET
        if any(word in title for word in ("waxed canvas n-1 deck jacket",)):
            return HSCodes.SHEEP_JACKET
        if any(word in title for word in ("flyer's club jacket waxed cotton",
                                          "japanese sateen", "carrier flight jacket",
                                          "sashiko crissman overshirt",
                                          "pilot jacket dry wax cotton",
                                          "pilot jacket cotton sashiko")):
            return HSCodes.COTTON_JACKET_OTHER
        if any(word in title for word in ("flight vest sateen",)):
            return HSCodes.COTTON_VEST
        if any(word in title for word in ("wool baseball cap", "1920 dkco. baseball cap")):
            return HSCodes.WOOL_HAT_OTHER
        if any(word in title for word in ("cotton baseball cap",)):
            return HSCodes.COTTON_CAP

    return None


def _get_hs_code_for_good_art(sku: str, title: str):
    """Get the US HTS Codes for Good Art"""
    if sku.startswith(StartSKU.GOOD_ART + "-"):
        if "silver" in title:
            if any(word in title for word in ("ring", "bracelet", "pendant", "rondel",
                                              "necklace", "belt loop buddy", "chain",
                                              "snap", "slider", "church key", "glasses loop",
                                              "balm cap")):
                return HSCodes.SILVER_JEWELRY
        if "brass" in title:
            if any(word in title for word in ("belt loop buddy")):
                return HSCodes.BRASS_KEY_HOOK
        if "custom order" in title:
            return HSCodes.SILVER_JEWELRY
        if "long sleeve t-shirt" in title:
            return HSCodes.COTTON_T_SHIRT
        if "army navy wallet" in title:
            return HSCodes.LEATHER_WALLET
        if "rubber biscuit rosette bracelet" in title:
            return HSCodes.SILVER_JEWELRY

    return None


def _get_hs_code_for_hollywood_trading_co(sku: str, title: str):
    """Get the US HTS Codes for Hollywood Trading Co"""
    if sku.startswith(StartSKU.HOLLYWOOD_TRADING_CO + "-"):
        if "belt" in title:
            return HSCodes.LEATHER_BELT
        if "medium wallet" in title:
            return HSCodes.LEATHER_WALLET
        if "wallet chain" in title:
            return HSCodes.STEEL_CHAIN
        if "brass key fob" in title:
            return HSCodes.BRASS_KEY_HOOK

    return None


def _get_hs_code_for_red_rabbit(sku: str, title: str):
    """Get the US HTS Codes for Red Rabbit"""
    if sku.startswith(StartSKU.RED_RABBIT + "-"):
        return HSCodes.SILVER_JEWELRY

    return None


def _get_hs_code_for_wesco(sku: str, title: str):
    """Get the US HTS Codes for Wesco"""
    if sku.startswith(StartSKU.WESCO + "-"):
        if "dressing bee seal plus" in title:
            return HSCodes.LEATHER_POLISH_OR_CREAM
        if any(word in title for word in ("dressing bee oil", "leather amore")):
            return HSCodes.LEATHER_OIL
        if "leather laces" in title:
            return HSCodes.LEATHER_SHOELACES
        if "nylon laces" in title:
            return HSCodes.OTHER_SHOELACES
        if "waxed laces" in title:
            return HSCodes.COTTON_SHOELACES
        if "flexfit cap" in title:
            return HSCodes.SYNTHETIC_CAP
        if "diamond logo hoodie" in title:
            return HSCodes.COTTON_SWEATSHIRT
        if any(word in title for word in ("engineer", "custom boss")):
            return HSCodes.ENGINEER_BOOTS_WELT
        if any(word in title for word in ("hendrik", "jobmaster", "warren", "morrison")):
            return HSCodes.WORK_BOOTS_WELT

    return None


def _get_hs_code_for_wigwam(sku: str, title: str):
    """Get the US HTS Codes for Wigwam"""
    if sku.startswith(StartSKU.WIGWAM + "-"):
        if any(word in title for word in ("work crew")):
            return HSCodes.COTTON_SOCKS
        if any(word in title for word in ("work durasole")):
            return HSCodes.SYNTHETIC_BLEND_SOCKS
        if any(word in title for word in ("wool workmate")):
            return HSCodes.WOOL_SOCKS

    return None

def _get_hs_code_for_other(sku: str, _: str):
    """Get the US HTS Codes for Other Products"""
    if sku.startswith("BEE-NATURAL"):
        return HSCodes.LEATHER_POLISH_OR_CREAM

    return None


_NON_IH_LOOKUPS = (
    _get_hs_code_for_bn3th,
    _get_hs_code_for_sacred_dog,
    _get_hs_code_for_simmons_bilt,
    _get_hs_code_for_obi,
    _get_hs_code_for_asahi,
    _get_hs_code_for_clutch,
    _get_hs_code_for_mustang,
    _get_hs_code_for_peanuts,
    _get_hs_code_for_porter,
    _get_hs_code_for_rats,
    _get_hs_code_for_utilitees,
    _get_hs_code_for_bee_natural,
    _get_hs_code_for_black_rock,
    _get_hs_code_for_dehen,
    _get_hs_code_for_good_art,
    _get_hs_code_for_hollywood_trading_co,
    _get_hs_code_for_red_rabbit,
    _get_hs_code_for_wesco,
    _get_hs_code_for_wigwam,
    _get_hs_code_for_other
)