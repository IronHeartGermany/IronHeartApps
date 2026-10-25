'''
Define the columns in the Shopify inventory CSV file.
'''

from enum import Enum, IntEnum, auto

class InventoryColumns(IntEnum):
    """ The column numbers of the Shopify Inventory report"""
    HANDLE = 0
    TITLE = 1
    OPTION1_NAME = 2
    OPTION1_VALUE = 3
    OPTION2_NAME = 4
    OPTION2_VALUE = 5
    OPTION3_NAME = 6
    OPTION3_VALUE = 7
    SKU = 8
    HS_CODE = 9
    COO = 10
    LOCATION = 11
    BIN_NAME = 12
    INCOMING = 13
    UNAVAILABLE = 14
    COMMITTED = 15
    AVAILABLE = 16
    ON_HAND_CURRENT = 17
    ON_HAND_NEW = 18
    VARIANT_PACKED_LENGTH = 19
    VARIANT_PACKED_WIDTH = 20
    VARIANT_PACKED_HEIGHT = 21
    VARIANT_PACKED_DIMENSION_UNIT = 22

class Field(Enum):
    """ Specify if a field is required, optional, or must be empty """
    REQUIRED = auto()
    OPTIONAL = auto()
    EMPTY = auto()


# Map header column index to a tuple containing the
# field name and if it's a required field
header_map : dict[int, (str, bool)] = {
    InventoryColumns.HANDLE: ("Handle", Field.REQUIRED),
    InventoryColumns.TITLE: ("Title", Field.REQUIRED),
    InventoryColumns.OPTION1_NAME: ("Option1 Name", Field.REQUIRED),
    InventoryColumns.OPTION1_VALUE: ("Option1 Value", Field.REQUIRED),
    InventoryColumns.OPTION2_NAME: ("Option2 Name", Field.EMPTY),
    InventoryColumns.OPTION2_VALUE: ("Option2 Value", Field.EMPTY),
    InventoryColumns.OPTION3_NAME: ("Option3 Name", Field.EMPTY),
    InventoryColumns.OPTION3_VALUE: ("Option3 Value", Field.EMPTY),
    InventoryColumns.SKU: ("SKU", Field.OPTIONAL),
    InventoryColumns.HS_CODE: ("HS Code", Field.REQUIRED),
    InventoryColumns.COO: ("COO", Field.REQUIRED),
    InventoryColumns.LOCATION: ("Location", Field.REQUIRED),
    InventoryColumns.BIN_NAME: ("Bin name", Field.EMPTY),
    InventoryColumns.INCOMING: ("Incoming (not editable)", Field.REQUIRED),
    InventoryColumns.UNAVAILABLE: ("Unavailable (not editable)", Field.REQUIRED),
    InventoryColumns.COMMITTED: ("Committed (not editable)", Field.REQUIRED),
    InventoryColumns.AVAILABLE: ("Available (not editable)", Field.REQUIRED),
    InventoryColumns.ON_HAND_CURRENT: ("On hand (current)", Field.REQUIRED),
    InventoryColumns.ON_HAND_NEW: ("On hand (new)", Field.EMPTY),
    InventoryColumns.VARIANT_PACKED_LENGTH: ("Variant Packed Length", Field.EMPTY),
    InventoryColumns.VARIANT_PACKED_WIDTH: ("Variant Packed Width", Field.EMPTY),
    InventoryColumns.VARIANT_PACKED_HEIGHT: ("Variant Packed Height", Field.EMPTY),
    InventoryColumns.VARIANT_PACKED_DIMENSION_UNIT: ("Variant Packed Dimension Unit", Field.EMPTY)
}
