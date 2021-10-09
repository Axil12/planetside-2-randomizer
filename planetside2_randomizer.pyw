import json
import random
import tkinter as tk
import os

class LoadoutRandomizer:
    FACTION_ID = {"vs": "1", "tr": "3", "nc": "2", "nso": "4"}
    SIDEARM_CATEGORY_ID = ["3", "24"]
    KNIFE_CATEGORY_ID = ["2"]
    GRENADE_CATEGORY_ID = ["17"]
    EXPLOSIVE_CATEGORY_ID = ["18"]
    ROCKET_LAUNCHER_CATEGORY_ID = ["13"]

    INTERCLASS_WEAPONS = [2, 3, 5, 17, 18, 24]
    INFILTRATOR_WEAPONS = INTERCLASS_WEAPONS + [11, 12, 19, 219]
    LIGHTASSAULT_WEAPONS = INTERCLASS_WEAPONS + [4, 8, 219]
    ENGINEER_WEAPONS = INTERCLASS_WEAPONS + [4, 8, 19]
    HEAVYASSAULT_WEAPONS = INTERCLASS_WEAPONS + [4, 6, 13, 14, 19]
    MEDIC_WEAPONS = INTERCLASS_WEAPONS + [4, 7, 19]
    MAX_WEAPONS = [9, 10, 14, 16, 20, 21, 22, 23]
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

    def __init__(self):
        self.config = {
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

        self.class_to_loadout_id = {
            "infiltrator": None,
            "light_assault": None,
            "heavy_assault": None,
            "combat_medic": None,
            "engineer": None,
            "max": None,
        }

        self.weapons = {}
        self.implants = []
        self.grenades = []
        self.suits = []
        self.utilities = []
        self.tacticals = []

        self.last_played_class = None

        self.load_config()

    def load_config(self):
        with open("config.json") as f:
            config = json.load(f)
        for key in config.keys():
            self.config[key] = config[key] # In case app_font is not in config.json

        with open("weapons.json") as f:
            self.weapons = json.load(f)

        with open("implants.json") as f:
            self.implants = json.load(f)

        with open("grenades.json") as f:
            self.grenades = json.load(f)

        with open("suits.json") as f:
            self.suits = json.load(f)

        with open("utilities.json") as f:
            self.utilities = json.load(f)

        with open("abilities.json") as f:
            self.abilities = json.load(f)

        with open("tacticals.json") as f:
            self.tacticals = json.load(f)

        faction = self.config["faction"]
        if faction not in ["nc", "tr", "vs", "nso"]:
            raise ValueError(
                'Wrong faction in the config file! Choose from ["nc", "tr", "vs", "nso"].'
            )
        if faction == "nc":
            self.class_to_loadout_id["infiltrator"] = "1"
            self.class_to_loadout_id["light_assault"] = "3"
            self.class_to_loadout_id["combat_medic"] = "4"
            self.class_to_loadout_id["engineer"] = "5"
            self.class_to_loadout_id["heavy_assault"] = "6"
            self.class_to_loadout_id["max"] = "7"
        elif faction == "tr":
            self.class_to_loadout_id["infiltrator"] = "8"
            self.class_to_loadout_id["light_assault"] = "10"
            self.class_to_loadout_id["combat_medic"] = "11"
            self.class_to_loadout_id["engineer"] = "12"
            self.class_to_loadout_id["heavy_assault"] = "13"
            self.class_to_loadout_id["max"] = "14"
        else:
            self.class_to_loadout_id["infiltrator"] = "15"
            self.class_to_loadout_id["light_assault"] = "17"
            self.class_to_loadout_id["combat_medic"] = "18"
            self.class_to_loadout_id["engineer"] = "19"
            self.class_to_loadout_id["heavy_assault"] = "20"
            self.class_to_loadout_id["max"] = "21"

        if not self.config["include_max"]:
            del self.class_to_loadout_id["max"]

    def draw_primary(self, class_, faction):
        class_id = self.class_to_loadout_id[class_]
        possible_weapon_categories = LoadoutRandomizer.LOADOUT_ALLOWED_WEAPONS[class_id]
        not_primaries_list = (
            LoadoutRandomizer.SIDEARM_CATEGORY_ID
            + LoadoutRandomizer.KNIFE_CATEGORY_ID
            + LoadoutRandomizer.GRENADE_CATEGORY_ID
            + LoadoutRandomizer.EXPLOSIVE_CATEGORY_ID
            + LoadoutRandomizer.ROCKET_LAUNCHER_CATEGORY_ID
        )
        possible_primary_categories = [
            id for id in possible_weapon_categories if str(id) not in not_primaries_list
        ]
        possible_weapons = []
        for key in self.weapons.keys():
            if "archer" in self.weapons[key]["name"].lower():
                if class_.lower() == "engineer":
                    possible_weapons.append(self.weapons[key])
                    continue
                else:
                    continue
            if not int(self.weapons[key]["item_category_id"]) in possible_primary_categories:
                continue
            if self.weapons[key]["faction_id"] not in [LoadoutRandomizer.FACTION_ID[faction], "0", None]:
                continue
            possible_weapons.append(self.weapons[key])
        drawn_primary_weapon = random.choice(possible_weapons)
        return drawn_primary_weapon

    def draw_secondary(self, class_, faction):
        class_id = self.class_to_loadout_id[class_]
        possible_weapons = []
        for key in self.weapons.keys():
            if not self.weapons[key]["item_category_id"] in LoadoutRandomizer.SIDEARM_CATEGORY_ID:
                continue
            if self.weapons[key]["faction_id"] not in [LoadoutRandomizer.FACTION_ID[faction], "0", None]:
                continue
            possible_weapons.append(self.weapons[key])
        drawn_secondary_weapon = random.choice(possible_weapons)
        return drawn_secondary_weapon

    def draw_rocket_launcher(self, faction):
        possible_weapons = []
        for key in self.weapons.keys():
            if self.weapons[key]["item_category_id"] != "13":
                continue
            if self.weapons[key]["faction_id"] not in [LoadoutRandomizer.FACTION_ID[faction], "0"]:
                continue
            possible_weapons.append(self.weapons[key])
        drawn_rocket_launcher = random.choice(possible_weapons)
        return drawn_rocket_launcher


    def draw_rocklet_type(self):
        possibilities = ["ACE Rocklet", "Sabot Rocklet", "Typhoon Rocklet"]
        return {"name": random.choice(possibilities)}


    def draw_implant(self, class_):
        drawn_implant = random.choice(self.implants)
        while (
            drawn_implant["class_restriction"] is not None
            and drawn_implant["class_restriction"].lower() != class_.lower()
        ):
            drawn_implant = random.choice(self.implants)
        return drawn_implant


    def draw_grenade(self, class_, faction):
        if class_.lower() == "max":
            return None
        drawn = random.choice(self.grenades)
        while drawn["class_restriction"] is not None and (
            class_.lower() not in drawn["class_restriction"]
            or drawn["faction"] not in ["0", LoadoutRandomizer.FACTION_ID[faction]]
        ):
            drawn = random.choice(self.grenades)
        return drawn


    def draw_knife(self, class_):
        if class_.lower() == "max":
            return "Max Fist"
        return random.choice(["Standard knife", "OHK knife", "AntiVehicle knife"])


    def draw_suit_slot(self, class_):
        if class_.lower() == "max":
            drawn = random.choice(self.suits)
            while (
                drawn["class_restriction"] is None
                or class_.lower() not in drawn["class_restriction"]
            ):
                drawn = random.choice(self.suits)
            return drawn

        drawn = random.choice(self.suits)
        while (
            drawn["class_restriction"] is not None
            and class_.lower() not in drawn["class_restriction"]
        ):
            drawn = random.choice(self.suits)
        return drawn


    def draw_utlity_slot(self, class_):
        if class_.lower() == "max":
            return None

        drawn = random.choice(self.utilities)
        while (
            drawn["class_restriction"] is not None
            and class_.lower() not in drawn["class_restriction"]
        ):
            drawn = random.choice(self.utilities)
        return drawn


    def draw_tactical_slot(self, class_):
        if class_.lower() == "max":
            return None
        return random.choice(self.tacticals)


    def draw_ability(self, class_, faction):
        drawn = random.choice(self.abilities)
        while drawn["class_restriction"] is not None and (
            class_.lower() not in drawn["class_restriction"]
            or drawn["faction"] not in ["0", LoadoutRandomizer.FACTION_ID[faction]]
        ):
            drawn = random.choice(self.abilities)
        return drawn


    def draw_loadout(self):
        drawn_class = random.choice(list(self.class_to_loadout_id.keys()))
        while drawn_class == self.last_played_class:
            drawn_class = random.choice(list(self.class_to_loadout_id.keys()))
        self.last_played_class = drawn_class

        drawn_class_id = self.class_to_loadout_id[drawn_class]

        drawn_primary_weapon = self.draw_primary(drawn_class, self.config["faction"])

        if drawn_class == "max":
            drawn_secondary_weapon = self.draw_primary(drawn_class, self.config["faction"])
        else:
            drawn_secondary_weapon = self.draw_secondary(drawn_class, self.config["faction"])

        if drawn_class == "max": # necessary since thumper is the same item category as grenade printer
            while "thumper" in drawn_primary_weapon["name"].lower():
                drawn_primary_weapon = self.draw_primary(drawn_class, self.config["faction"])
            while "thumper" in drawn_secondary_weapon["name"].lower():
                drawn_secondary_weapon = self.draw_primary(drawn_class, self.config["faction"])

        drawn_tertiary_weapon = None
        if drawn_class == "heavy_assault":
            drawn_tertiary_weapon = self.draw_rocket_launcher(self.config["faction"])
        elif drawn_class == "light_assault":
            drawn_tertiary_weapon = self.draw_rocklet_type()

        draw_implant_1, draw_implant_2 = self.draw_implant(drawn_class), self.draw_implant(
            drawn_class
        )
        while draw_implant_2 == draw_implant_1:
            draw_implant_2 = self.draw_implant(drawn_class)

        drawn_grenade = self.draw_grenade(drawn_class, self.config["faction"])
        drawn_knife = self.draw_knife(drawn_class)
        drawn_suit_slot = self.draw_suit_slot(drawn_class)
        drawn_utility_slot = self.draw_utlity_slot(drawn_class)
        drawn_tactical_slot = self.draw_tactical_slot(drawn_class)
        drawn_ability = self.draw_ability(drawn_class, self.config["faction"])

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

    def run_tk_display(self):
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

        font = self.config["app_font"]
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
            drawn_loadout = self.draw_loadout()
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
        if self.config["ability"]:
            ability_indic.pack(anchor="w")
            ability_label.pack(anchor="e")
        if self.config["implants"]:
            implant_1_indic.pack(anchor="w")
            implant_2_indic.pack(anchor="w")
            implant_1_label.pack(anchor="e")
            implant_2_label.pack(anchor="e")
        if self.config["grenade"]:
            grenade_indic.pack(anchor="w")
            grenade_label.pack(anchor="e")
        if self.config["knife"]:
            knife_indic.pack(anchor="w")
            knife_label.pack(anchor="e")
        if self.config["suit_slot"]:
            suit_slot_indic.pack(anchor="w")
            suit_slot_label.pack(anchor="e")
        if self.config["utility_slot"]:
            utility_slot_indic.pack(anchor="w")
            utility_slot_label.pack(anchor="e")
        if self.config["tactical_slot"]:
            tactical_slot_indic.pack(anchor="w")
            tactical_slot_label.pack(anchor="e")

        draw_button.pack(anchor="e")

        display_draw()

        window.mainloop()

def main():
    lr = LoadoutRandomizer()
    lr.run_tk_display()

if __name__ == "__main__":
    main()
