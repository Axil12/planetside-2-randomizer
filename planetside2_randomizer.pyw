import json
import random
import tkinter as tk
import os

CONFIG = {
    "faction": None,
    "include_max": None,
    "implants": None,
    "suit_slot": None,
    "utility_slot": None,
    "ability": None,
    "grenade": None,
    "knife": None,
    "tactical_slot": None,
    "app_font": "Helvetica 9",
}

FACTION_ID = {"vs": "1", "tr": "3", "nc": "2", "nso": None}
CLASS_TO_LOADOUT_ID = {
    "infiltrator": None,
    "light_assault": None,
    "heavy_assault": None,
    "combat_medic": None,
    "engineer": None,
    "max": None,
}

SIDEARM_CATEGORY_ID = ["3", "24"]
KNIFE_CATEGORY_ID = ["2"]
GRENADE_CATEGORY_ID = ["17"]
EXPLOSIVE_CATEGORY_ID = ["18"]
ROCKET_LAUNCHER_CATEGORY_ID = ["13"]

INTERCLASS_WEAPONS = [2, 3, 5, 17, 18, 24]
INFILTRATOR_WEAPONS = INTERCLASS_WEAPONS + [11, 12, 19]
LIGHTASSAULT_WEAPONS = INTERCLASS_WEAPONS + [4, 8]
ENGINEER_WEAPONS = INTERCLASS_WEAPONS + [4, 8, 19]
HEAVYASSAULT_WEAPONS = INTERCLASS_WEAPONS + [4, 6, 13, 14, 19]
MEDIC_WEAPONS = INTERCLASS_WEAPONS + [4, 7, 19]
MAX_WEAPONS = [9, 10, 16, 20, 21, 22, 23]
LOADOUT_ALLOWED_WEAPONS = {
    "1": INFILTRATOR_WEAPONS,
    "8": INFILTRATOR_WEAPONS,
    "15": INFILTRATOR_WEAPONS,
    "3": LIGHTASSAULT_WEAPONS,
    "10": LIGHTASSAULT_WEAPONS,
    "17": LIGHTASSAULT_WEAPONS,
    "4": MEDIC_WEAPONS,
    "11": MEDIC_WEAPONS,
    "18": MEDIC_WEAPONS,
    "5": ENGINEER_WEAPONS,
    "12": ENGINEER_WEAPONS,
    "19": ENGINEER_WEAPONS,
    "6": HEAVYASSAULT_WEAPONS,
    "13": HEAVYASSAULT_WEAPONS,
    "20": HEAVYASSAULT_WEAPONS,
    "7": MAX_WEAPONS,
    "14": MAX_WEAPONS,
    "21": MAX_WEAPONS,
}

WEAPONS = {}
IMPLANTS = []
GRENADES = []
SUITS = []
UTILITIES = []
TACTICALS = []

last_played_class = None


def load_config():
    with open("config.json") as f:
        config = json.load(f)
    for key in config.keys():
        CONFIG[key] = config[key]

    global WEAPONS
    with open("weapons.json") as f:
        WEAPONS = json.load(f)

    global IMPLANTS
    with open("implants.json") as f:
        IMPLANTS = json.load(f)

    global GRENADES
    with open("grenades.json") as f:
        GRENADES = json.load(f)

    global SUITS
    with open("suits.json") as f:
        SUITS = json.load(f)

    global UTILITIES
    with open("utilities.json") as f:
        UTILITIES = json.load(f)

    global ABILITIES
    with open("abilities.json") as f:
        ABILITIES = json.load(f)

    global TACTICALS
    with open("tacticals.json") as f:
        TACTICALS = json.load(f)

    faction = CONFIG["faction"]
    if faction not in ["nc", "tr", "vs", "nso"]:
        raise ValueError(
            'Wrong faction in the config file! Choose from ["nc", "tr", "vs", "nso"].'
        )
    if faction == "nc":
        CLASS_TO_LOADOUT_ID["infiltrator"] = "1"
        CLASS_TO_LOADOUT_ID["light_assault"] = "3"
        CLASS_TO_LOADOUT_ID["combat_medic"] = "4"
        CLASS_TO_LOADOUT_ID["engineer"] = "5"
        CLASS_TO_LOADOUT_ID["heavy_assault"] = "6"
        CLASS_TO_LOADOUT_ID["max"] = "7"
    elif faction == "tr":
        CLASS_TO_LOADOUT_ID["infiltrator"] = "8"
        CLASS_TO_LOADOUT_ID["light_assault"] = "10"
        CLASS_TO_LOADOUT_ID["combat_medic"] = "11"
        CLASS_TO_LOADOUT_ID["engineer"] = "12"
        CLASS_TO_LOADOUT_ID["heavy_assault"] = "13"
        CLASS_TO_LOADOUT_ID["max"] = "14"
    else:
        CLASS_TO_LOADOUT_ID["infiltrator"] = "15"
        CLASS_TO_LOADOUT_ID["light_assault"] = "17"
        CLASS_TO_LOADOUT_ID["combat_medic"] = "18"
        CLASS_TO_LOADOUT_ID["engineer"] = "19"
        CLASS_TO_LOADOUT_ID["heavy_assault"] = "20"
        CLASS_TO_LOADOUT_ID["max"] = "21"

    if not config["include_max"]:
        del CLASS_TO_LOADOUT_ID["max"]


def draw_primary(class_id, faction):
    possible_weapon_categories = LOADOUT_ALLOWED_WEAPONS[class_id]
    not_primaries_list = (
        SIDEARM_CATEGORY_ID
        + KNIFE_CATEGORY_ID
        + GRENADE_CATEGORY_ID
        + EXPLOSIVE_CATEGORY_ID
        + ROCKET_LAUNCHER_CATEGORY_ID
    )
    possible_primary_categories = [
        id for id in possible_weapon_categories if str(id) not in not_primaries_list
    ]
    possible_weapons = []
    for key in WEAPONS.keys():
        if not int(WEAPONS[key]["item_category_id"]) in possible_primary_categories:
            continue
        if WEAPONS[key]["faction_id"] not in [FACTION_ID[faction], "0", None]:
            continue
        possible_weapons.append(WEAPONS[key])
    drawn_primary_weapon = random.choice(possible_weapons)
    return drawn_primary_weapon


def draw_secondary(class_id, faction):
    possible_weapons = []
    for key in WEAPONS.keys():
        if not WEAPONS[key]["item_category_id"] in SIDEARM_CATEGORY_ID:
            continue
        if WEAPONS[key]["faction_id"] not in [FACTION_ID[faction], "0", None]:
            continue
        possible_weapons.append(WEAPONS[key])
    drawn_secondary_weapon = random.choice(possible_weapons)
    return drawn_secondary_weapon


def draw_rocket_launcher(faction):
    possible_weapons = []
    for key in WEAPONS.keys():
        if WEAPONS[key]["item_category_id"] != "13":
            continue
        if WEAPONS[key]["faction_id"] not in [FACTION_ID[faction], "0"]:
            continue
        possible_weapons.append(WEAPONS[key])
    drawn_rocket_launcher = random.choice(possible_weapons)
    return drawn_rocket_launcher


def draw_rocklet_type():
    possibilities = ["ACE Rocklet", "Sabot Rocklet", "Typhoon Rocklet"]
    return {"name": random.choice(possibilities)}


def draw_implant(class_):
    drawn_implant = random.choice(IMPLANTS)
    while (
        drawn_implant["class_restriction"] is not None
        and drawn_implant["class_restriction"].lower() != class_.lower()
    ):
        drawn_implant = random.choice(IMPLANTS)
    return drawn_implant


def draw_grenade(class_, faction):
    if class_.lower() == "max":
        return None
    drawn = random.choice(GRENADES)
    while drawn["class_restriction"] is not None and (
        class_.lower() not in drawn["class_restriction"]
        or drawn["faction"] not in ["0", FACTION_ID[faction]]
    ):
        drawn = random.choice(GRENADES)
    return drawn


def draw_knife(class_):
    if class_.lower() == "max":
        return "Max Fist"
    return random.choice(["Standard knife", "OHK knife", "AntiVehicle knife"])


def draw_suit_slot(class_):
    if class_.lower() == "max":
        drawn = random.choice(SUITS)
        while (
            drawn["class_restriction"] is None
            or class_.lower() not in drawn["class_restriction"]
        ):
            drawn = random.choice(SUITS)
        return drawn

    drawn = random.choice(SUITS)
    while (
        drawn["class_restriction"] is not None
        and class_.lower() not in drawn["class_restriction"]
    ):
        drawn = random.choice(SUITS)
    return drawn


def draw_utlity_slot(class_):
    if class_.lower() == "max":
        return None

    drawn = random.choice(UTILITIES)
    while (
        drawn["class_restriction"] is not None
        and class_.lower() not in drawn["class_restriction"]
    ):
        drawn = random.choice(UTILITIES)
    return drawn


def draw_tactical_slot(class_, faction):
    if class_.lower() == "max":
        return None
    return random.choice(TACTICALS)


def draw_ability(class_, faction):
    drawn = random.choice(ABILITIES)
    while drawn["class_restriction"] is not None and (
        class_.lower() not in drawn["class_restriction"]
        or drawn["faction"] not in ["0", FACTION_ID[faction]]
    ):
        drawn = random.choice(ABILITIES)
    return drawn


def draw_loadout():
    global last_played_class
    drawn_class = random.choice(list(CLASS_TO_LOADOUT_ID.keys()))
    while drawn_class == last_played_class:
        drawn_class = random.choice(list(CLASS_TO_LOADOUT_ID.keys()))
    last_played_class = drawn_class

    drawn_class_id = CLASS_TO_LOADOUT_ID[drawn_class]

    drawn_primary_weapon = draw_primary(drawn_class_id, CONFIG["faction"])

    if drawn_class == "max":
        drawn_secondary_weapon = draw_primary(drawn_class_id, CONFIG["faction"])
    else:
        drawn_secondary_weapon = draw_secondary(drawn_class_id, CONFIG["faction"])

    drawn_tertiary_weapon = None
    if drawn_class == "heavy_assault":
        drawn_tertiary_weapon = draw_rocket_launcher(CONFIG["faction"])
    elif drawn_class == "light_assault":
        drawn_tertiary_weapon = draw_rocklet_type()

    draw_implant_1, draw_implant_2 = draw_implant(drawn_class), draw_implant(
        drawn_class
    )
    while draw_implant_2 == draw_implant_1:
        draw_implant_2 = draw_implant(drawn_class)

    drawn_grenade = draw_grenade(drawn_class, CONFIG["faction"])
    drawn_knife = draw_knife(drawn_class)
    drawn_suit_slot = draw_suit_slot(drawn_class)
    drawn_utility_slot = draw_utlity_slot(drawn_class)
    drawn_tactical_slot = draw_tactical_slot(drawn_class, CONFIG["faction"])
    drawn_ability = draw_ability(drawn_class, CONFIG["faction"])

    drawn_loadout = {
        "class": drawn_class,
        "primary": drawn_primary_weapon,
        "secondary": drawn_secondary_weapon,
        "tertiary": drawn_tertiary_weapon,
        "implant_1": draw_implant_1,
        "implant_2": draw_implant_2,
        "grenade": drawn_grenade,
        "knife": drawn_knife,
        "suit_slot": drawn_suit_slot,
        "utility_slot": drawn_utility_slot,
        "tactical_slot": drawn_tactical_slot,
        "ability": drawn_ability,
    }

    return drawn_loadout


def main():
    load_config()

    window = tk.Tk()
    window.minsize(300, 0)
    window.maxsize(500, 0)
    window.title("Loadout Randomizer")
    if os.path.isfile("EDIM_logo.ico"):
        window.iconbitmap("EDIM_logo.ico")

    Frame_top = tk.Frame(window, borderwidth=10)
    Frame_top.pack(side=tk.TOP)
    Frame_0 = tk.Frame(Frame_top, borderwidth=10)
    Frame_0.pack(side=tk.LEFT, anchor="w")
    Frame_1 = tk.Frame(Frame_top, borderwidth=10)
    Frame_1.pack(side=tk.RIGHT, anchor="e")
    Frame_2 = tk.Frame(window, borderwidth=10)
    Frame_2.pack(side=tk.BOTTOM)

    font = CONFIG["app_font"]
    class_indic = tk.Label(
        Frame_0, font=font + " bold", justify=tk.LEFT, text="Class : "
    )
    primary_indic = tk.Label(
        Frame_0, font=font + " bold", justify=tk.LEFT, text="1st Weapon : "
    )
    secondary_indic = tk.Label(
        Frame_0, font=font + " bold", justify=tk.LEFT, text="2nd Weapon : "
    )
    tertiary_indic = tk.Label(
        Frame_0, font=font + " bold", justify=tk.LEFT, text="3rd Weapon : "
    )
    ability_indic = tk.Label(
        Frame_0, font=font + " bold", justify=tk.LEFT, text="Ability : "
    )
    implant_1_indic = tk.Label(
        Frame_0, font=font + " bold", justify=tk.LEFT, text="Implant 1 : "
    )
    implant_2_indic = tk.Label(
        Frame_0, font=font + " bold", justify=tk.LEFT, text="Implant 2 : "
    )
    grenade_indic = tk.Label(
        Frame_0, font=font + " bold", justify=tk.LEFT, text="Grenade : "
    )
    knife_indic = tk.Label(
        Frame_0, font=font + " bold", justify=tk.LEFT, text="Knife : "
    )
    suit_slot_indic = tk.Label(
        Frame_0, font=font + " bold", justify=tk.LEFT, text="Suit : "
    )
    utility_slot_indic = tk.Label(
        Frame_0, font=font + " bold", justify=tk.LEFT, text="Utility : "
    )
    tactical_slot_indic = tk.Label(
        Frame_0, font=font + " bold", justify=tk.LEFT, text="Tactical : "
    )

    class_label = tk.Label(Frame_1, font=font + " bold", justify=tk.RIGHT)
    primary_label = tk.Label(Frame_1, font=font, justify=tk.RIGHT)
    secondary_label = tk.Label(Frame_1, font=font, justify=tk.RIGHT)
    tertiary_label = tk.Label(Frame_1, font=font, justify=tk.RIGHT)
    ability_label = tk.Label(Frame_1, font=font, justify=tk.RIGHT)
    implant_1_label = tk.Label(Frame_1, font=font, justify=tk.RIGHT)
    implant_2_label = tk.Label(Frame_1, font=font, justify=tk.RIGHT)
    grenade_label = tk.Label(Frame_1, font=font, justify=tk.RIGHT)
    knife_label = tk.Label(Frame_1, font=font, justify=tk.RIGHT)
    suit_slot_label = tk.Label(Frame_1, font=font, justify=tk.RIGHT)
    utility_slot_label = tk.Label(Frame_1, font=font, justify=tk.RIGHT)
    tactical_slot_label = tk.Label(Frame_1, font=font, justify=tk.RIGHT)

    def display_draw():
        drawn_loadout = draw_loadout()
        class_label["text"] = f'{drawn_loadout["class"].capitalize().replace("_", " ")}'
        primary_label["text"] = f'{drawn_loadout["primary"]["name"]}'
        secondary_label["text"] = f'{drawn_loadout["secondary"]["name"]}'
        tertiary_label["text"] = (
            f" "
            if drawn_loadout["tertiary"] is None
            else drawn_loadout["tertiary"]["name"]
        )
        ability_label["text"] = f'{drawn_loadout["ability"]["name"]}'
        implant_1_label["text"] = f'{drawn_loadout["implant_1"]["name"]}'
        implant_2_label["text"] = f'{drawn_loadout["implant_2"]["name"]}'
        grenade_label["text"] = (
            ""
            if drawn_loadout["grenade"] is None
            else f'{drawn_loadout["grenade"]["name"]}'
        )
        knife_label["text"] = (
            " " if drawn_loadout["knife"] is None else f'{drawn_loadout["knife"]}'
        )
        suit_slot_label["text"] = f'{drawn_loadout["suit_slot"]["name"]}'
        utility_slot_label["text"] = (
            " "
            if drawn_loadout["utility_slot"] is None
            else f'{drawn_loadout["utility_slot"]["name"]}'
        )
        tactical_slot_label["text"] = (
            ""
            if drawn_loadout["tactical_slot"] is None
            else f'{drawn_loadout["tactical_slot"]}'
        )

    if os.path.isfile("button_img.png"):
        button_img = tk.PhotoImage(file="button_img.png").subsample(2, 2)
        draw_button = tk.Button(
            Frame_2, command=display_draw, image=button_img, borderwidth=0
        )
    else:
        draw_button = tk.Button(
            Frame_2,
            height=2,
            width=15,
            text="Draw loadout",
            font=font + " bold",
            background="gray",
            command=display_draw,
        )

    class_indic.pack(anchor="w")
    primary_indic.pack(anchor="w")
    secondary_indic.pack(anchor="w")
    tertiary_indic.pack(anchor="w")
    class_label.pack(anchor="e")
    primary_label.pack(anchor="e")
    secondary_label.pack(anchor="e")
    tertiary_label.pack(anchor="e")
    if CONFIG["ability"]:
        ability_indic.pack(anchor="w")
        ability_label.pack(anchor="e")
    if CONFIG["implants"]:
        implant_1_indic.pack(anchor="w")
        implant_2_indic.pack(anchor="w")
        implant_1_label.pack(anchor="e")
        implant_2_label.pack(anchor="e")
    if CONFIG["grenade"]:
        grenade_indic.pack(anchor="w")
        grenade_label.pack(anchor="e")
    if CONFIG["knife"]:
        knife_indic.pack(anchor="w")
        knife_label.pack(anchor="e")
    if CONFIG["suit_slot"]:
        suit_slot_indic.pack(anchor="w")
        suit_slot_label.pack(anchor="e")
    if CONFIG["utility_slot"]:
        utility_slot_indic.pack(anchor="w")
        utility_slot_label.pack(anchor="e")
    if CONFIG["tactical_slot"]:
        tactical_slot_indic.pack(anchor="w")
        tactical_slot_label.pack(anchor="e")

    draw_button.pack(anchor="e")

    display_draw()

    window.mainloop()


if __name__ == "__main__":
    main()
