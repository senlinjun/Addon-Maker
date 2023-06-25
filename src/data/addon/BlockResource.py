from data.addon.basic_component import BasicComponent
import json, lib


class Sound(BasicComponent):
    def __init__(self, content, ui_system):
        super(Sound, self).__init__("sound", content, ui_system)
        self.lang = self.content.addon.MainSystem.lang
        self.sounds = []
        with open("./data/addon/sounds.json", "r") as f:
            self.sounds = json.load(f)
        self.sound = "wood"

    def parse(self, component_value):
        self.sound = component_value

    def generate(self):
        return self.sound

    def getUiDict(self):
        return {self.lang["addon", "sound_name"]: (self.sound, "combobox", self.sounds)}

    def write(self, pack_dict):
        pack_dict[self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        self.sound = lib.getWidgetValue(ui_dict[self.lang["addon", "sound_name"]])


class Isotropic(BasicComponent):
    def __init__(self, content, ui_system):
        super(Isotropic, self).__init__("isotropic", content, ui_system)
        self.lang = self.content.addon.MainSystem.lang
        self.ways = {"down": False, "up": False}
        self.side = {"east": False, "north": False, "south": False, "west": False}
        self.select_all = 0
        self.side_select_all = 0

    def parse(self, component_value):
        if isinstance(component_value, bool):
            for way in self.ways:
                self.ways[way] = component_value
            for s in self.side:
                self.side[s] = component_value
        elif isinstance(component_value, dict):
            for key in component_value:
                if key in ["up", "down"]:
                    self.ways[key] = component_value[key]
                elif key == "side":
                    for s in self.side:
                        self.side[s] = component_value[key]
                elif key in ["east", "north", "south", "west"]:
                    self.side[key] = component_value[key]

    def generate(self):
        return_data = {"up": self.ways["up"], "down": self.ways["down"]}
        flag = self.side["south"]
        for s in self.side:
            if self.side[s] != flag:
                flag = None
                break
        if flag is None:
            for s in self.side:
                return_data[s] = self.side[s]
        else:
            return_data["side"] = flag

        flag = return_data["up"]
        for key in return_data:
            if return_data[key] != flag:
                flag = None
                break

        if flag is not None:
            return flag
        return return_data

    def getUiDict(self):
        flag = self.ways["up"]
        side_flag = self.side["north"]
        for key in self.ways:
            if self.ways[key] != flag:
                flag = None
                break
        for key in self.side:
            if self.side[key] != side_flag:
                side_flag = None
                break
        if side_flag is None or side_flag != flag:
            flag = None
        if flag is not None:
            if flag:
                self.select_all = 2
            else:
                self.select_all = 0
        else:
            self.select_all = 1
        if side_flag is not None:
            if side_flag:
                self.side_select_all = 2
            else:
                self.side_select_all = 0
        else:
            self.side_select_all = 1

        return {
            self.lang["ui", "select_all"]: (self.select_all, "tristate", None),
            self.lang["addon", "up"]: (self.ways["up"], "bool", None),
            self.lang["addon", "down"]: (self.ways["down"], "bool", None),
            self.lang["addon", "side"]: {
                self.lang["ui", "select_all"]: (self.side_select_all, "tristate", None),
                self.lang["addon", "east"]: (self.side["east"], "bool", None),
                self.lang["addon", "west"]: (self.side["west"], "bool", None),
                self.lang["addon", "south"]: (self.side["south"], "bool", None),
                self.lang["addon", "north"]: (self.side["north"], "bool", None),
            },
        }

    def write(self, pack_dict):
        pack_dict[self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        for way in self.ways:
            self.ways[way] = lib.getWidgetValue(ui_dict[self.lang["addon", way]])
        for s in self.side:
            self.side[s] = lib.getWidgetValue(
                ui_dict[self.lang["addon", "side"]][self.lang["addon", s]]
            )

        value = lib.getWidgetValue(ui_dict[self.lang["ui", "select_all"]])
        if value != self.select_all:
            if value == 1:
                value = 2
            for way in self.ways:
                self.ways[way] = bool(value)
            for s in self.side:
                self.side[s] = bool(value)
            return

        side_value = lib.getWidgetValue(
            ui_dict[self.lang["addon", "side"]][self.lang["ui", "select_all"]]
        )
        if side_value != self.side_select_all:
            if side_value == 1:
                side_value = 2
            for s in self.side:
                self.side[s] = bool(side_value)
            return


class BrightnessGamma(BasicComponent):
    def __init__(self, content, ui_system):
        super(BrightnessGamma, self).__init__("brightness_gamma", content, ui_system)
        self.lang = self.content.addon.MainSystem.lang
        self.value = 0.0

    def parse(self, component_value):
        self.value = component_value

    def generate(self):
        return self.value

    def getUiDict(self):
        return {
            self.lang["addon", "brightness_gamma_name"]: (
                self.value,
                "float",
                (0.0, 1.0, 0.01),
            )
        }

    def write(self, pack_dict):
        pack_dict[self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        self.value = lib.getWidgetValue(
            ui_dict[self.lang["addon", "brightness_gamma_name"]]
        )


components = {
    "sound": Sound,
    "isotropic": Isotropic,
    "brightness_gamma": BrightnessGamma,
}
