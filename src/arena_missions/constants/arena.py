from functools import lru_cache
from pathlib import Path
from typing import Literal

import orjson


OfficeLayout = Literal[
    "OfficeLayout1",
    "OfficeLayout1B",
    "OfficeLayout1C",
    "OfficeLayout3",
    "OfficeLayout1_mirror",
    "OfficeLayout1B_mirror",
    "OfficeLayout1C_mirror",
    "OfficeLayout3_mirror",
]

OfficeRoom = Literal[
    "BreakRoom",
    "MainOffice",
    "SmallOffice",
    "Lab1",
    "Lab2",
    "Hallway",
    "Reception",
    "Warehouse",
]

ObjectIds = Literal[
    "ActionFigure",
    "AP_Bld_Ceiling_Aircon_01",
    "AP_Bld_Wall_Glass_Large_Door_01",
    "AP_Item_Tape_01",
    "AP_Item_Tool_Board",
    "AP_Prop_Barrel_Open_01",
    "AP_Prop_Barrel_Water_01",
    "AP_Prop_Bin_Rubbish_01",
    "AP_Prop_Bucket_02",
    "AP_Prop_Cabinets_01",
    "AP_Prop_CardboardBox_Open_05",
    "AP_Prop_CardboardBox_Stack_02",
    "AP_Prop_Cellotape_01",
    "AP_Prop_CorkBoard_02",
    "AP_Prop_Couch_02",
    "AP_Prop_Couch_06",
    "AP_Prop_Desk_Blue",
    "AP_Prop_Desk_Green_model",
    "AP_Prop_Desk_Green",
    "AP_Prop_Desk_Red_model",
    "AP_Prop_Desk_Red",
    "AP_Prop_Desk_Yellow",
    "AP_Prop_Fire_Extinguisher_01",
    "AP_Prop_Folder_PVC_02",
    "AP_Prop_Generator_Large_02",
    "AP_Prop_Lab_Clamp_02_Arm_01",
    "AP_Prop_Lab_MachinePanel_01",
    "AP_Prop_Lab_MachinePanel_02",
    "AP_Prop_Lab_Tank_01",
    "AP_Prop_Lab_Tank_02",
    "AP_Prop_Minigolf_Ball_01",
    "AP_Prop_Minigolf_Club_01",
    "AP_Prop_Note_05",
    "AP_Prop_PaperTray_01_Full_01",
    "AP_Prop_Pen_01",
    "AP_Prop_Pen_03",
    "AP_Prop_Pen_06",
    "AP_Prop_Photocopier_01",
    "AP_Prop_Plant_01",
    "AP_Prop_Plant_09",
    "AP_Prop_Print_Tube_01",
    "AP_Prop_Safety_Barrier_02",
    "AP_Prop_Shelf_06",
    "AP_Prop_Shelf_Wall_04",
    "AP_Prop_Shelf_Wall_FreezeRay",
    "AP_Prop_Shelf_Wall_Laser",
    "AP_Prop_Sign_OutofOrder_01",
    "AP_Prop_Target_Circle_01",
    "AP_Prop_Whiteboard_Devices_03",
    "AP_Prop_Whiteboard_Devices_04",
    "AP_Prop_Whiteboard_Devices_05",
    "AP_Prop_Whiteboard_Devices_06",
    "AP_Prop_Whiteboard_Devices_07",
    "AP_Prop_Whiteboard_Devices_08",
    "AP_Prop_Whiteboard_Devices_09",
    "AP_Prop_Whiteboard_Devices_10",
    "AP_Prop_Whiteboard_Devices_11",
    "AP_Prop_Whiteboard_Devices_12",
    "AP_Prop_Whiteboard_Devices_13",
    "AP_Prop_Whiteboard_Devices_14",
    "AP_Prop_Whiteboard_Devices_15",
    "AP_Tool_Buffer_01_Battery",
    "Apple",
    "AppleSlice_01",
    "Banana_01",
    "BananaBunch_01",
    "Bookshelf_Wooden_01",
    "Bowl_01",
    "BreadLoaf",
    "BreadSlice_01",
    "Broken_Cord_01",
    "Burger_04",
    "CableFrayed_01",
    "Cake_02",
    "CakeSlice_02",
    "CandyBar_01",
    "CandyJar_01",
    "CanSoda_01",
    "CanSodaNew_01",
    "CanSodaNew_Crushed_01",
    "CanSodaNew_Open_01",
    "Carrot_01",
    "Cereal_Box_01",
    "CoffeeBeans_01",
    "CoffeeCup_Lid_01",
    "CoffeeCup_Open_Empty_01",
    "CoffeeCup_Open_Empty_02",
    "CoffeeMaker_01",
    "CoffeeMug_Boss",
    "CoffeeMug_Yellow",
    "CoffeePot_01",
    "CoffeeUnMaker_01",
    "ColorChanger_Button_Blue",
    "ColorChanger_Button_Green",
    "ColorChanger_Button_Red",
    "ColorChangerStation",
    "Computer_Monitor_01",
    "Computer_Monitor_Broken",
    "Computer_Monitor_New",
    "CounterBase_03",
    "Cutting_Board",
    "Dart",
    "DartBoard",
    "Deembiggenator_Crates",
    "Desk_01",
    "DeskFan_Broken_01",
    "DeskFan_New_01",
    "Donut_01",
    "Door_01",
    "EAC_Machine",
    "Embiggenator",
    "EmptyPaperTray",
    "FireAlarm_01",
    "FireExtinguisher_01",
    "Floppy_AntiVirus_Broken",
    "Floppy_AntiVirus",
    "Floppy_Virus_Broken",
    "Floppy_Virus",
    "FoodPlate_01",
    "Fork_01",
    "Fork_Lift",
    "ForkLift",
    "FreezeRay",
    "FridgeLower_02",
    "FridgeUpper_02",
    "FulllPaperTray_01",
    "FuseBox_01_Lever",
    "FuseBox_01",
    "FuseBox_02",
    "GravityPad",
    "Hammer",
    "Handsaw",
    "Jar_Jam_01",
    "Jar_PeanutButter_01",
    "Keyboard",
    "KitchenCabinet_01_Trapped",
    "KitchenCabinet_01",
    "KitchenCabinet_02",
    "KitchenCounter01",
    "KitchenCounterBase_02",
    "KitchenCounterBase_03",
    "KitchenCounterDrawer_02",
    "KitchenCounterDrawer_03",
    "KitchenCounterSink_01",
    "KitchenCounterTop_02",
    "KitchenStool_01",
    "Knife_01",
    "Lab_Terminal",
    "Laser_CircuitBoard",
    "Laser_ControlPanel",
    "Laser_Tip_Broken",
    "Laser_Tip",
    "Laser",
    "LaserBase_toy",
    "LightSwitch_01",
    "Manager_Chair",
    "ManagerDesk",
    "Microwave_01",
    "MilkCarton_01",
    "MissionItemHolder",
    "Office_Chair",
    "PackingBox",
    "PaperCup_01",
    "PaperCup_Crushed_01",
    "PBJ_Sandwich",
    "Pear_01",
    "PieFruit_01",
    "PieFruitSlice_01",
    "PinBoard_01",
    "PinBoard_02",
    "PortalGenerator",
    "PowerOutlet_01",
    "Printer_3D",
    "Printer_Cartridge_Figure",
    "Printer_Cartridge_Hammer",
    "Printer_Cartridge_Lever",
    "Printer_Cartridge_Mug",
    "Printer_Cartridge",
    "Radio_01_Broken",
    "Radio_01",
    "ReceptionDesk",
    "Record_01",
    "RoboticArm_01",
    "SafetyBarrier_02",
    "SandwichHalf_01",
    "Screwdriver",
    "Security_Button",
    "Shelf_01",
    "Shelves_Tall_01",
    "sign_diamond_carrot",
    "sign_diamond_fire",
    "sign_diamond_freeze",
    "sign_diamond_gravity",
    "sign_diamond_laser",
    "sign_diamond_quantum",
    "sign_diamond_shrink",
    "sign_office_layout_1",
    "sign_short_breakroom_1",
    "sign_short_breakroom_2",
    "sign_short_caution_carrot",
    "sign_short_caution_electrical",
    "sign_short_caution_gravity_1",
    "sign_short_caution_gravity_2",
    "sign_short_caution_quantum_1",
    "sign_short_caution_quantum_2",
    "sign_short_caution_restricted_1",
    "sign_short_caution_shrink",
    "sign_short_office_1",
    "sign_short_poster_delwan_1",
    "sign_short_poster_delwan_2",
    "sign_short_poster_delwan_3",
    "sign_short_poster_delwan_4",
    "sign_short_poster_tam",
    "sign_short_quantum_1",
    "sign_short_quantum_2",
    "sign_short_robotics_1",
    "sign_short_robotics_2",
    "sign_short_warehouse_1",
    "sign_square_breakroom",
    "sign_tall_caution_carrot",
    "sign_tall_caution_electrical",
    "sign_tall_caution_freeze",
    "sign_tall_caution_laser",
    "sign_tall_caution_robotics",
    "sign_tall_caution_shrink",
    "sign_tall_poster_tam_1",
    "sign_tall_poster_tam_2",
    "SK_Veh_Pickup_01_ToolBox",
    "SM_Bld_Door_02",
    "SM_Bld_Wall_Metal_Slide_02",
    "SM_Bld_Wall_Window_Blinds_Open_04",
    "SM_Item_Clipboard_01",
    "SM_Prop_AirVent_01",
    "SM_Prop_AirVent_Wall_01",
    "SM_Prop_Book_Group_01",
    "SM_Prop_Book_Group_02",
    "SM_Prop_Book_Group_03",
    "SM_Prop_Book_Group_04",
    "SM_Prop_Book_Group_05",
    "SM_Prop_Book_Group_06",
    "SM_Prop_Book_Group_07",
    "SM_Prop_Book_Group_08",
    "SM_Prop_Book_Magazine_01",
    "SM_Prop_Book_Phone_Open_01",
    "SM_Prop_Buttons_02",
    "SM_Prop_Buttons_05",
    "SM_Prop_Calender_01",
    "SM_Prop_Cart_01",
    "SM_Prop_Certificate_01",
    "SM_Prop_Crate_Stack_01",
    "SM_Prop_Drink_Dispenser_01",
    "SM_Prop_FlatPackCardboardBoxes_03",
    "SM_Prop_FlatPackCardboardBoxes_04",
    "SM_Prop_Folder_Holder_01",
    "SM_Prop_Folder_Holder_02",
    "SM_Prop_Folder_Holder_03",
    "SM_Prop_Folder_Holder_04",
    "SM_Prop_Folder_Manila_01",
    "SM_Prop_Folder_Manila_02",
    "SM_Prop_Folder_Manila_03",
    "SM_Prop_Folder_Manila_04",
    "SM_Prop_Folder_PVC_01",
    "SM_Prop_Folder_PVC_02",
    "SM_Prop_FolderTray_01",
    "SM_Prop_FolderTray_02",
    "SM_Prop_FolderTray_03",
    "SM_Prop_FolderTray_04",
    "SM_Prop_Lighting_Cable_Bulb_01",
    "SM_Prop_NetCable_03",
    "SM_Prop_NotePad_01",
    "SM_Prop_Oxygen_Tank Water",
    "SM_Prop_Oxygen_Tank_Large",
    "SM_Prop_Oxygen_Tank",
    "SM_Prop_PalletStack_02",
    "SM_Prop_Paper_04",
    "SM_Prop_Paper_05",
    "SM_Prop_Paper_06",
    "SM_Prop_Paper_Pile_01",
    "SM_Prop_Paper_Pile_03",
    "SM_Prop_Papers_01",
    "SM_Prop_PaperTray_01_Full_01",
    "SM_Prop_Plastic_Pipe_Spool_01",
    "SM_Prop_PowerBoxes_01",
    "SM_Prop_Powercable_01",
    "SM_Prop_Powercable_02",
    "SM_Prop_Powercable_03",
    "SM_Prop_Scales_01",
    "SM_Prop_Server_Cabinet_01",
    "SM_Prop_Server_Node_01",
    "SM_Prop_Table_02",
    "SM_Prop_ToolBox_01",
    "SM_Prop_Warehouse_Boxes_Stacked_03",
    "SM_Prop_Warehouse_Boxes_Stacked_04",
    "SM_Prop_Warehouse_Light_04",
    "SM_Prop_Warehouse_Platform_Trolley_01",
    "SM_Prop_Wirespool_01",
    "SM_Prop_Wirespool_Small_01",
    "SM_Sign_Exit_02",
    "SM_Tool_Buffer_01_Battery",
    "SM_Tool_Drill_Chuck_01",
    "SM_Tool_Handsaw_01",
    "Spoon_01",
    "StickyNote",
    "Table_Metal_01",
    "TableRound_02",
    "TableRoundSmall_02",
    "TAMPrototypeHead_01",
    "TeslaCoil_Small",
    "TeslaCoil",
    "Toast_01",
    "Toast_02",
    "Toast_03",
    "Toast_04_Jam",
    "Toast_04_PBJ",
    "Toast_04",
    "Toaster_02",
    "ToyBed",
    "TrashCan_01",
    "Trophy01",
    "Unassigned",
    "V_Monitor_Embiggenator",
    "V_Monitor_FreezeRay",
    "V_Monitor_Gravity",
    "V_Monitor_Laser",
    "V_Monitor_Portal",
    "VendingMachine_01_B4_Button",
    "VendingMachine_01_E5_Button",
    "VendingMachine_01_E7_Button",
    "VendingMachine_01_M8_Button",
    "VendingMachine_01",
    "WallClock_01",
    "Warehouse_Boxes",
    "WarningSign_01",
    "WaterCooler_01",
    "WaterPuddle_01",
    "WhiteBoard_01",
    "Whiteboard_CoffeeUnmaker",
    "Whiteboard_YesterdayMachine",
    "YesterdayMachine_01",
]


ObjectColor = Literal[
    "Black",
    "Blue",
    "Brown",
    "Green",
    "Gray",
    "Red",
    "Yellow",
]

ColorChangerObjectColor = Literal[
    "Red",
    "Green",
    "Blue",
]

# ObjectStateName = Literal[
#     "isPickedUp",
#     "isBroken",
#     "isScanned",
#     "isOpen",
#     "isToggledOn",
#     "isPowered",
#     "isUsed",
#     "isCut",
#     "isEaten",
#     "isHot",
#     "isCold",
#     "isFilled",
#     "isDirty",
#     "isCooked",
#     "isSparking",
#     "isEmbiggenated",
#     "isOverloaded",
#     "isExamined",
#     "isColorChanged",
#     # Only works on receptacles
#     "isEmpty",
#     # Will only work for the emotion tester
#     "isNeutral",
#     "isHappy",
#     "isSad",
#     "isAngry",
#     "isScared",
# ]

RequiredObjectStateName = Literal[
    "isToggledOn",
    "isOpen",
    "isFilled",
    "isHot",
    "isCold",
    "isCooked",
    "isCut",
    "isDirty",
    "isBroken",
    "isEaten",
    "isSparking",
    "isOverloaded",
    # Will only work for the emotion tester
    "isNeutral",
    "isHappy",
    "isSad",
    "isAngry",
    "isScared",
    # isLocked only works on Doors
    "isLocked",
    # Only works on receptacles
    "isEmpty",
    # Empties receptacles on challenge start
    "removeInitialContainedItems",
    # Ensures the object is infected, I don't know why this is different to the goal state
    "Infected",
    # Prevents the object from spawning normally
    "Blacklist",
    # Ensures it is the only object of its type
    "Unique",
    # Removes the object if it exists from some other definition
    "Removed",
    # I don't know what circuits and power does, and I don't think it matters since all circuits
    # seem to be disabled or global
    "circuitId",
    "generateCircuitId",
    "generatePower",
]

GoalStateExpressionKey = Literal[
    "isInfected",
    # Will only work for the emotion tester
    "isNeutral",
    "isHappy",
    "isSad",
    "isAngry",
    "isScared",
]


BooleanStr = Literal["true", "false"]
SpawnRelation = Literal["in"]
FluidType = Literal["Water", "Milk", "Coffee", "None"]


@lru_cache(maxsize=1)
def load_object_id_to_readable_name_map() -> dict[ObjectIds, str]:
    """Load mapping of Object ID to a readable name."""
    json_file = Path(__file__).parent.joinpath("object_id_to_readable_name.json")
    mapping = orjson.loads(json_file.read_bytes())
    return mapping


@lru_cache(maxsize=1)
def get_all_readable_names() -> list[str]:
    """Get all the readable names."""
    return list(set(load_object_id_to_readable_name_map().values()))


def is_readable_name(name: str) -> bool:
    """Check if the name is a readable name."""
    return name in get_all_readable_names()
