from data.addon.basic_component import BasicComponent
import lib


class BasicEventResponse(BasicComponent):
    def __init__(self, identifier, content, ui_system, event):
        super(BasicEventResponse, self).__init__(identifier, content, ui_system)
        self.event = event

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["events"][self.event][
            self.identifier
        ] = self.generate()


class AddMobEffect(BasicEventResponse):
    def __init__(self, content, ui_system, event):
        super(AddMobEffect, self).__init__("add_mob_effect", content, ui_system, event)
        self.amplifier = 0
        self.duration = 0.0
        self.effect = ""
        self.target = "self"

    def parse(self, component_value):
        self.amplifier = component_value["amplifier"]
        self.duration = component_value["duration"]
        self.effect = component_value["effect"]
        self.target = component_value["target"]

    def generate(self):
        return {
            "amplifier": self.amplifier,
            "duration": self.duration,
            "effect": self.effect,
            "target": self.target,
        }

    def getUiDict(self):
        return {
            self.lang["addon", "add_mob_effect_amplifier"]: (
                self.amplifier,
                "int",
                None,
            ),
            self.lang["addon", "add_mob_effect_duration"]: (
                self.duration,
                "float",
                None,
            ),
            self.lang["addon", "add_mob_effect_effect"]: (self.effect, "str", None),
            self.lang["addon", "target"]: (self.target, "str", None),
        }

    def parseFromUi(self, ui_dict):
        self.amplifier = lib.getWidgetValue(
            ui_dict[self.lang["addon", "add_mob_effect_amplifier"]]
        )
        self.duration = lib.getWidgetValue(
            ui_dict[self.lang["addon", "add_mob_effect_duration"]]
        )
        self.effect = lib.getWidgetValue(
            ui_dict[self.lang["addon", "add_mob_effect_effect"]]
        )
        self.target = lib.getWidgetValue(ui_dict[self.lang["addon", "target"]])
        self.updateUi(ui_dict, self.getUiDict())


responses = {"add_mob_effect": AddMobEffect}
