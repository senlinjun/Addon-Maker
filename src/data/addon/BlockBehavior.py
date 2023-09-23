from data.addon.basic_component import BasicComponent
from PyQt5.QtWidgets import QInputDialog, QMessageBox
import lib


class CollisionBox(BasicComponent):
    def __init__(self, content, ui_system):
        super(CollisionBox, self).__init__(
            "minecraft:collision_box", content, ui_system
        )
        self.enable = True
        self.origin_x, self.origin_y, self.origin_z = -8.0, 0.0, -8.0
        self.size_x, self.size_y, self.size_z = 16.0, 16.0, 16.0

    def parse(self, component_value):
        if isinstance(component_value, bool):
            self.enable = component_value
        elif isinstance(component_value, dict):
            self.enable = True
            self.origin_x, self.origin_y, self.origin_z = component_value["origin"]
            self.size_x, self.size_y, self.size_z = component_value["size"]

    def generate(self):
        if not self.enable:
            return False
        if [self.origin_x, self.origin_y, self.origin_z] == [-8.0, 0.0, -8.0] and [
            self.size_x,
            self.size_y,
            self.size_z,
        ] == [16.0, 16.0, 16.0]:
            return True
        return {
            "origin": [self.origin_x, self.origin_y, self.origin_z],
            "size": [self.size_x, self.size_y, self.size_z],
        }

    def getUiDict(self):
        if not self.enable:
            return {
                self.lang["addon", "minecraft:collision_box_enable"]: (
                    self.enable,
                    "bool",
                    None,
                )
            }
        return {
            self.lang["addon", "minecraft:collision_box_enable"]: (
                self.enable,
                "bool",
                None,
            ),
            self.lang["addon", "minecraft:collision_box_origin"]: {
                "x": (self.origin_x, "float", (-8, 8)),
                "y": (self.origin_y, "float", (0, 16)),
                "z": (self.origin_z, "float", (-8, 8)),
            },
            self.lang["addon", "minecraft:collision_box_size"]: {
                "x": (self.size_x, "float", (-8, 16)),
                "y": (self.size_y, "float", (0, 16)),
                "z": (self.size_z, "float", (-8, 16)),
            },
        }

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["components"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        self.enable = lib.getWidgetValue(
            ui_dict[self.lang["addon", "minecraft:collision_box_enable"]]
        )

        if self.lang["addon", "minecraft:collision_box_origin"] in ui_dict:
            self.origin_x = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:collision_box_origin"]]["x"]
            )
            self.origin_y = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:collision_box_origin"]]["y"]
            )
            self.origin_z = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:collision_box_origin"]]["z"]
            )
        if self.lang["addon", "minecraft:collision_box_size"] in ui_dict:
            self.size_x = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:collision_box_size"]]["x"]
            )
            self.size_y = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:collision_box_size"]]["y"]
            )
            self.size_z = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:collision_box_size"]]["z"]
            )
            if self.origin_x + self.size_x > 8:
                self.size_x = 8 - self.origin_x
            if self.origin_y + self.size_y > 16:
                self.size_y = 16 - self.origin_y
            if self.origin_z + self.size_z > 8:
                self.size_z = 8 - self.origin_z
            if self.origin_x + self.size_x < -8:
                self.size_x = -8 - self.origin_x
            if self.origin_y + self.size_y < 0:
                self.size_y = -self.origin_y
            if self.origin_z + self.size_z < -8:
                self.size_z = -8 - self.origin_z
        self.updateUi(ui_dict, self.getUiDict())


class DestructibleByExplosion(BasicComponent):
    def __init__(self, content, ui_system):
        super(DestructibleByExplosion, self).__init__(
            "minecraft:destructible_by_explosion", content, ui_system
        )

        self.enable = True
        self.explosion_resistance = 0.0

    def parse(self, component_value):
        if isinstance(component_value, bool):
            self.enable = component_value

        elif isinstance(component_value, dict):
            self.enable = True
            self.explosion_resistance = component_value["explosion_resistance"]

    def generate(self):
        if not self.enable:
            return False
        elif self.enable and self.explosion_resistance == 0.0:
            return True

        return {"explosion_resistance": self.explosion_resistance}

    def getUiDict(self):
        if not self.enable:
            return {
                self.lang["addon", "minecraft:destructible_by_explosion_enable"]: (
                    self.enable,
                    "bool",
                    None,
                )
            }
        return {
            self.lang["addon", "minecraft:destructible_by_explosion_enable"]: (
                self.enable,
                "bool",
                None,
            ),
            self.lang[
                "addon", "minecraft:destructible_by_explosion_explosion_resistance"
            ]: (self.explosion_resistance, "float", None),
        }

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["components"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        if self.lang["addon", "minecraft:destructible_by_explosion_enable"] in ui_dict:
            self.enable = lib.getWidgetValue(
                ui_dict[
                    self.lang["addon", "minecraft:destructible_by_explosion_enable"]
                ]
            )
            if (
                self.enable
                and self.lang[
                    "addon", "minecraft:destructible_by_explosion_explosion_resistance"
                ]
                in ui_dict
            ):
                self.explosion_resistance = lib.getWidgetValue(
                    ui_dict[
                        self.lang[
                            "addon",
                            "minecraft:destructible_by_explosion_explosion_resistance",
                        ]
                    ]
                )
        self.updateUi(ui_dict, self.getUiDict())


class DestructibleByMining(BasicComponent):
    def __init__(self, content, ui_system):
        super(DestructibleByMining, self).__init__(
            "minecraft:destructible_by_mining", content, ui_system
        )

        self.enable = True
        self.seconds_to_destroy = 0.0

    def parse(self, component_value):
        if isinstance(component_value, bool):
            self.enable = component_value
        elif isinstance(component_value, dict):
            self.enable = True
            self.seconds_to_destroy = component_value["seconds_to_destroy"]

    def generate(self):
        if not self.enable:
            return False
        if self.enable and self.seconds_to_destroy == 0.0:
            return True
        return {"seconds_to_destroy": self.seconds_to_destroy}

    def getUiDict(self):
        if not self.enable:
            return {
                self.lang["addon", "minecraft:destructible_by_mining_enable"]: (
                    self.enable,
                    "bool",
                    None,
                )
            }
        return {
            self.lang["addon", "minecraft:destructible_by_mining_enable"]: (
                self.enable,
                "bool",
                None,
            ),
            self.lang["addon", "minecraft:destructible_by_mining_seconds"]: (
                self.seconds_to_destroy,
                "float",
                None,
            ),
        }

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["components"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        if self.lang["addon", "minecraft:destructible_by_mining_enable"] in ui_dict:
            self.enable = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:destructible_by_mining_enable"]]
            )
            if (
                self.enable
                and self.lang["addon", "minecraft:destructible_by_mining_seconds"]
                in ui_dict
            ):
                self.seconds_to_destroy = lib.getWidgetValue(
                    ui_dict[
                        self.lang["addon", "minecraft:destructible_by_mining_seconds"]
                    ]
                )
        self.updateUi(ui_dict, self.getUiDict())


class DisplayName(BasicComponent):
    def __init__(self, content, ui_system):
        super(DisplayName, self).__init__("minecraft:display_name", content, ui_system)

        self.name = ""

    def parse(self, component_value):
        self.name = component_value

    def generate(self):
        return self.name

    def getUiDict(self):
        return {
            self.lang["addon", "minecraft:display_name_name"]: (self.name, "str", None)
        }

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["components"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        self.name = lib.getWidgetValue(
            ui_dict[self.lang["addon", "minecraft:display_name_name"]]
        )
        self.updateUi(ui_dict, self.getUiDict())


class Flammable(BasicComponent):
    def __init__(self, content, ui_system):
        super(Flammable, self).__init__("minecraft:flammable", content, ui_system)

        self.enable = False
        self.catch_chance_modifier = 5
        self.destroy_chance_modifier = 20

    def parse(self, component_value):
        if isinstance(component_value, bool):
            self.enable = component_value
            return
        self.enable = True
        self.catch_chance_modifier = component_value["catch_chance_modifier"]
        self.destroy_chance_modifier = component_value["destroy_chance_modifier"]

    def generate(self):
        if not self.enable:
            return False

        if (
            self.catch_chance_modifier == 5
            and self.destroy_chance_modifier == 20
            and self.enable
        ):
            return True

        return {
            "catch_chance_modifier": self.catch_chance_modifier,
            "destroy_chance_modifier": self.destroy_chance_modifier,
        }

    def getUiDict(self):
        if not self.enable:
            return {
                self.lang["addon", "minecraft:flammable_enable"]: (
                    self.enable,
                    "bool",
                    None,
                )
            }
        return {
            self.lang["addon", "minecraft:flammable_enable"]: (
                self.enable,
                "bool",
                None,
            ),
            self.lang["addon", "minecraft:flammable_catch_chance_modifier"]: (
                self.catch_chance_modifier,
                "int",
                None,
            ),
            self.lang["addon", "minecraft:flammable_destroy_chance_modifier"]: (
                self.destroy_chance_modifier,
                "int",
                None,
            ),
        }

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["components"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        if self.lang["addon", "minecraft:flammable_enable"] in ui_dict:
            self.enable = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:flammable_enable"]]
            )
        if self.lang["addon", "minecraft:flammable_catch_chance_modifier"] in ui_dict:
            self.catch_chance_modifier = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:flammable_catch_chance_modifier"]]
            )
        if self.lang["addon", "minecraft:flammable_destroy_chance_modifier"] in ui_dict:
            self.destroy_chance_modifier = lib.getWidgetValue(
                ui_dict[
                    self.lang["addon", "minecraft:flammable_destroy_chance_modifier"]
                ]
            )
        self.updateUi(ui_dict, self.getUiDict())


class Friction(BasicComponent):
    def __init__(self, content, ui_system):
        super(Friction, self).__init__("minecraft:friction", content, ui_system)

        self.friction = 0.6

    def parse(self, component_value):
        self.friction = component_value

    def generate(self):
        return self.friction

    def getUiDict(self):
        return {
            self.lang["addon", "minecraft:friction_value"]: (
                self.friction,
                "float",
                (0.00, 0.99, 0.01),
            )
        }

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["components"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        self.friction = lib.getWidgetValue(
            ui_dict[self.lang["addon", "minecraft:friction_value"]]
        )
        self.updateUi(ui_dict, self.getUiDict())


class MapColor(BasicComponent):
    def __init__(self, content, ui_system):
        super(MapColor, self).__init__("minecraft:map_color", content, ui_system)

        self.color = "#FFFFFF"

    def parse(self, component_value):
        self.color = component_value

    def generate(self):
        return self.color

    def getUiDict(self):
        return {
            self.lang["addon", "minecraft:map_color_color"]: (self.color, "str", None)
        }

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["components"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        self.color = lib.getWidgetValue(
            ui_dict[self.lang["addon", "minecraft:map_color_color"]]
        )
        self.updateUi(ui_dict, self.getUiDict())


class LightDampening(BasicComponent):
    def __init__(self, content, ui_system):
        super(LightDampening, self).__init__(
            "minecraft:light_dampening", content, ui_system
        )

        self.value = 15

    def parse(self, component_value):
        self.value = component_value

    def generate(self):
        return self.value

    def getUiDict(self):
        return {
            self.lang["addon", "minecraft:light_dampening_name"]: (
                self.value,
                "int",
                (0, 15),
            )
        }

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["components"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        self.value = lib.getWidgetValue(
            ui_dict[self.lang["addon", "minecraft:light_dampening_name"]]
        )
        self.updateUi(ui_dict, self.getUiDict())


class LightEmission(BasicComponent):
    def __init__(self, content, ui_system):
        super(LightEmission, self).__init__(
            "minecraft:light_emission", content, ui_system
        )

        self.value = 0

    def parse(self, component_value):
        self.value = component_value

    def generate(self):
        return self.value

    def getUiDict(self):
        return {
            self.lang["addon", "minecraft:light_emission_name"]: (
                self.value,
                "int",
                (0, 15),
            )
        }

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["components"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        self.value = lib.getWidgetValue(
            ui_dict[self.lang["addon", "minecraft:light_emission_name"]]
        )
        self.updateUi(ui_dict, self.getUiDict())


class SelectionBox(BasicComponent):
    def __init__(self, content, ui_system):
        super(SelectionBox, self).__init__(
            "minecraft:selection_box", content, ui_system
        )

        self.origin_x, self.origin_y, self.origin_z = -8.0, 0.0, -8.0
        self.size_x, self.size_y, self.size_z = 16.0, 16.0, 16.0
        self.enable = True

    def parse(self, component_value):
        if isinstance(component_value, bool):
            self.enable = component_value
            return
        self.enable = True
        self.origin_x, self.origin_y, self.origin_z = component_value["origin"]
        self.size_x, self.size_y, self.size_z = component_value["size"]

    def generate(self):
        if not self.enable:
            return False
        if [self.origin_x, self.origin_y, self.origin_z] == [-8.0, 0.0, -8.0] and [
            self.size_x,
            self.size_y,
            self.size_z,
        ] == [16.0, 16.0, 16.0]:
            return True
        return {
            "origin": [self.origin_x, self.origin_y, self.origin_z],
            "size": [self.size_x, self.size_y, self.size_z],
        }

    def getUiDict(self):
        if not self.enable:
            return {
                self.lang["addon", "minecraft:selection_box_enable"]: (
                    self.enable,
                    "bool",
                    None,
                )
            }
        return {
            self.lang["addon", "minecraft:selection_box_enable"]: (
                self.enable,
                "bool",
                None,
            ),
            self.lang["addon", "minecraft:selection_box_origin"]: {
                "x": (self.origin_x, "float", (-8, 8)),
                "y": (self.origin_y, "float", (0, 16)),
                "z": (self.origin_z, "float", (-8, 8)),
            },
            self.lang["addon", "minecraft:selection_box_size"]: {
                "x": (self.size_x, "float", (-8, 16)),
                "y": (self.size_y, "float", (0, 16)),
                "z": (self.size_z, "float", (-8, 16)),
            },
        }

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["components"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        self.enable = lib.getWidgetValue(
            ui_dict[self.lang["addon", "minecraft:selection_box_enable"]]
        )

        if self.lang["addon", "minecraft:selection_box_origin"] in ui_dict:
            self.origin_x = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:selection_box_origin"]]["x"]
            )
            self.origin_y = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:selection_box_origin"]]["y"]
            )
            self.origin_z = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:selection_box_origin"]]["z"]
            )
        if self.lang["addon", "minecraft:selection_box_size"] in ui_dict:
            self.size_x = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:selection_box_size"]]["x"]
            )
            self.size_y = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:selection_box_size"]]["y"]
            )
            self.size_z = lib.getWidgetValue(
                ui_dict[self.lang["addon", "minecraft:selection_box_size"]]["z"]
            )
            if self.origin_x + self.size_x > 8:
                self.size_x = 8 - self.origin_x
            if self.origin_y + self.size_y > 16:
                self.size_y = 16 - self.origin_y
            if self.origin_z + self.size_z > 8:
                self.size_z = 8 - self.origin_z
            if self.origin_x + self.size_x < -8:
                self.size_x = -8 - self.origin_x
            if self.origin_y + self.size_y < 0:
                self.size_y = -self.origin_y
            if self.origin_z + self.size_z < -8:
                self.size_z = -8 - self.origin_z
        self.updateUi(ui_dict, self.getUiDict())


class IsExperimental(BasicComponent):
    def __init__(self, content, ui_system):
        super(IsExperimental, self).__init__("is_experimental", content, ui_system)

        self.value = False

    def parse(self, component_value):
        self.value = component_value

    def generate(self):
        return self.value

    def getUiDict(self):
        return {self.lang["addon", "is_experimental_name"]: (self.value, "bool", None)}

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["description"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        self.value = lib.getWidgetValue(
            ui_dict[self.lang["addon", "is_experimental_name"]]
        )
        self.updateUi(ui_dict, self.getUiDict())


class Properties(BasicComponent):
    def __init__(self, content, ui_system):
        super(Properties, self).__init__("properties", content, ui_system)

        self.properties = {}

    def parse(self, component_value):
        self.properties = component_value

    def generate(self):
        return self.properties

    def getUiDict(self):
        back_dict = {}
        for key in self.properties:
            back_dict[key] = (self.properties[key], "list", None)
        back_dict[self.lang["addon", "properties_operate"]] = {
            self.lang["addon", "properties_operate_add"]: (
                self.add,
                "button",
                self.lang["addon", "properties_operate_add"],
            ),
            self.lang["addon", "properties_operate_remove"]: (
                self.remove,
                "button",
                self.lang["addon", "properties_operate_remove"],
            ),
        }
        return back_dict

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["description"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        ui_dict.pop(self.lang["addon", "properties_operate"])
        for list_name in ui_dict:
            self.properties[list_name] = lib.getWidgetValue(ui_dict[list_name])
        self.updateUi(ui_dict, self.getUiDict())

    def add(self):
        ask_new_property = QInputDialog.getText(
            self.ui_system,
            self.lang["ui", "input"],
            self.lang["addon", "properties_ask_new"],
        )
        if not ask_new_property[1]:
            return
        new_property = ask_new_property[0]
        if new_property.find(" ") != -1:
            QMessageBox.critical(
                self.ui_system,
                self.ui_system.MainSystem.lang["ui", "error"],
                self.ui_system.MainSystem.lang["ui", "cannot_contain_spaces"],
            )
            return
        if new_property == "":
            QMessageBox.critical(
                self.ui_system,
                self.ui_system.MainSystem.lang["ui", "error"],
                self.ui_system.MainSystem.lang["ui", "cannot_leave_blank"],
            )
            return
        self.properties[new_property] = []
        self.ui_system.ui.showComponent()

    def remove(self):
        items = [i for i in self.properties.keys()]
        ask_remove_item = QInputDialog.getItem(
            self.ui_system,
            self.lang["ui", "input"],
            self.lang["addon", "properties_ask_remove"],
            items,
            editable=False,
        )
        if not ask_remove_item[1]:
            return
        remove_item = ask_remove_item[0]
        if remove_item not in self.properties:
            return
        self.properties.pop(remove_item)
        self.ui_system.ui.showComponent()


class RegisterToCreativeMenu(BasicComponent):
    def __init__(self, content, ui_system):
        super(RegisterToCreativeMenu, self).__init__(
            "register_to_creative_menu", content, ui_system
        )

        self.value = False

    def parse(self, component_value):
        self.value = component_value

    def generate(self):
        return self.value

    def getUiDict(self):
        return {
            self.lang["addon", "register_to_creative_menu_name"]: (
                self.value,
                "bool",
                None,
            )
        }

    def write(self, pack_dict):
        pack_dict["minecraft:block"]["description"][self.identifier] = self.generate()

    def parseFromUi(self, ui_dict):
        self.value = lib.getWidgetValue(
            ui_dict[self.lang["addon", "register_to_creative_menu_name"]]
        )
        self.updateUi(ui_dict, self.getUiDict())


components = {
    "minecraft:collision_box": CollisionBox,
    "minecraft:destructible_by_explosion": DestructibleByExplosion,
    "minecraft:destructible_by_mining": DestructibleByMining,
    "minecraft:display_name": DisplayName,
    "minecraft:flammable": Flammable,
    "minecraft:friction": Friction,
    "minecraft:map_color": MapColor,
    "minecraft:light_dampening": LightDampening,
    "minecraft:selection_box": SelectionBox,
    "is_experimental": IsExperimental,
    "properties": Properties,
    "register_to_creative_menu": RegisterToCreativeMenu,
}
# TODO crafting_table,geometry,loot,placement_filter,transformation,unit_cube
