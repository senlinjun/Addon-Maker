from data.addon.basic_component import BasicComponent
import lib


class BasicTrigger(BasicComponent):
    def __init__(self, identifier, content, ui_system):
        super(BasicTrigger, self).__init__(identifier, content, ui_system)
        self.condition = ""
        self.event = ""
        self.target = "self"

    def parse(self, component_value):
        if "condition" in component_value:
            self.condition = component_value["condition"]
        if "event" in component_value:
            self.event = component_value["event"]
        if "target" in component_value:
            self.target = component_value["target"]

    def generate(self):
        back_dict = {}
        if self.condition != "":
            back_dict["condition"] = self.condition
        if self.event != "":
            back_dict["event"] = self.event
        if self.target != "self":
            back_dict["target"] = self.target
        return back_dict

    def getUiDict(self):
        events = [event for event in self.content.events.keys()]
        events.append(self.lang["addon", "none"])
        event = self.event
        if self.event == "":
            event = self.lang["addon", "none"]
        return {
            self.lang["addon", "condition"]: (self.condition, "str", None),
            self.lang["addon", "event"]: (event, "combobox", events),
            self.lang["addon", "target"]: (self.target, "str", None),
        }

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["components"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        self.condition = lib.getWidgetValue(ui_dict[self.lang["addon", "condition"]])
        event = lib.getWidgetValue(ui_dict[self.lang["addon", "event"]])
        if event == self.lang["addon", "none"]:
            event = ""
        self.event = event
        self.target = lib.getWidgetValue(ui_dict[self.lang["addon", "target"]])


class OnFallOn(BasicTrigger):
    def __init__(self, content, ui_system):
        super(OnFallOn, self).__init__("minecraft:on_fall_on", content, ui_system)
        self.min_fall_distance = 0.0

    def parse(self, component_value):
        if "condition" in component_value:
            self.condition = component_value["condition"]
        if "event" in component_value:
            self.event = component_value["event"]
        if "min_fall_distance" in component_value:
            self.min_fall_distance = component_value["min_fall_distance"]
        if "target" in component_value:
            self.target = component_value["target"]

    def generate(self):
        back_dict = {}
        if self.condition != "":
            back_dict["condition"] = self.condition
        if self.event != "":
            back_dict["event"] = self.event
        if self.min_fall_distance != 0.0:
            back_dict["min_fall_distance"] = self.min_fall_distance
        if self.target != "self":
            back_dict["target"] = self.target
        return back_dict

    def getUiDict(self):
        events = [event for event in self.content.events.keys()]
        events.append(self.lang["addon","none"])
        event = self.event
        if self.event == "":
            event = self.lang["addon","none"]
        return {
            self.lang["addon", "condition"]: (self.condition, "str", None),
            self.lang["addon", "event"]: (event, "combobox", events),
            self.lang["addon", "target"]: (self.target, "str", None),
            self.lang["addon", "minecraft:on_fall_on_min_fall_distance"]: (
                self.min_fall_distance,
                "float",
                None,
            ),
        }

    def parseFromUi(self, ui_dict):
        self.condition = lib.getWidgetValue(ui_dict[self.lang["addon", "condition"]])
        event = lib.getWidgetValue(ui_dict[self.lang["addon", "event"]])
        if event == self.lang["addon","none"]:
            event = ""
        self.event = event
        self.target = lib.getWidgetValue(ui_dict[self.lang["addon", "target"]])
        self.min_fall_distance = lib.getWidgetValue(
            ui_dict[self.lang["addon", "minecraft:on_fall_on_min_fall_distance"]]
        )


class OnInteract(BasicTrigger):
    def __init__(self, content, ui_system):
        super(OnInteract, self).__init__("minecraft:on_interact", content, ui_system)


class OnPlaced(BasicTrigger):
    def __init__(self, content, ui_system):
        super(OnPlaced, self).__init__("minecraft:on_placed", content, ui_system)


class OnPlayerDestroyed(BasicTrigger):
    def __init__(self, content, ui_system):
        super(OnPlayerDestroyed, self).__init__(
            "minecraft:on_player_destroyed", content, ui_system
        )


class OnPlayerPlacing(BasicTrigger):
    def __init__(self, content, ui_system):
        super(OnPlayerPlacing, self).__init__(
            "minecraft:on_player_placing", content, ui_system
        )


class OnStepOn(BasicTrigger):
    def __init__(self, content, ui_system):
        super(OnStepOn, self).__init__("minecraft:on_step_on", content, ui_system)


class OnStepOff(BasicTrigger):
    def __init__(self, content, ui_system):
        super(OnStepOff, self).__init__("minecraft:on_step_off", content, ui_system)


class QueuedTicking(BasicTrigger):
    def __init__(self, content, ui_system):
        super(QueuedTicking, self).__init__(
            "minecraft:queued_ticking", content, ui_system
        )
        self.condition = ""
        self.event = ""
        self.target = "self"
        self.interval_range_a = 0
        self.interval_range_b = 0
        self.looping = True

    def parse(self, component_value):
        if "condition" in component_value:
            self.condition = component_value["condition"]
        if "event" in component_value:
            self.event = component_value["event"]
        if "target" in component_value:
            self.target = component_value["target"]

    def generate(self):
        back_dict = {}
        if self.condition != "":
            back_dict["condition"] = self.condition
        if self.event != "":
            back_dict["event"] = self.event
        if self.target != "self":
            back_dict["target"] = self.target
        return back_dict

    def getUiDict(self):
        events = [event for event in self.content.events.keys()]
        return {
            self.lang["addon", "condition"]: (self.condition, "str", None),
            self.lang["addon", "event"]: (self.event, "combobox", events),
            self.lang["addon", "target"]: (self.target, "str", None),
        }

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["components"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        self.condition = lib.getWidgetValue(ui_dict[self.lang["addon", "condition"]])
        self.event = lib.getWidgetValue(ui_dict[self.lang["addon", "event"]])
        self.target = lib.getWidgetValue(ui_dict[self.lang["addon", "target"]])


triggers = {
    "minecraft:on_fall_on": OnFallOn,
    "minecraft:on_interact": OnInteract,
    "minecraft:on_placed": OnPlaced,
    "minecraft:on_player_destroyed": OnPlayerDestroyed,
    "minecraft:on_player_placing": OnPlayerPlacing,
    "minecraft:on_step_on": OnStepOn,
    "minecraft:on_step_off": OnStepOff,
}
# minecraft:queued_ticking,minecraftt:random_ticking
