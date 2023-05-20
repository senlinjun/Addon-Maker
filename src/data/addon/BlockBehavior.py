from data.addon.basic_component import BasicComponent
import lib

class CollisionBox(BasicComponent):
    def __init__(self):
        super(CollisionBox, self).__init__("minecraft:collision_box")
        self.enable = True
        self.origin_x,self.origin_y,self.origin_z = -8.0,0.0,-8.0
        self.size_x, self.size_y, self.size_z = 16.0, 16.0, 16.0

    def parse(self,component_value):
        if isinstance(component_value,bool):
            self.enable = component_value
        elif isinstance(component_value,dict):
            self.enable = True
            self.origin_x,self.origin_y,self.origin_z = component_value["origin"]
            self.size_x, self.size_y, self.size_z = component_value["size"]

    def generate(self):
        if not self.enable:
            return False
        if [self.origin_x,self.origin_y,self.origin_z] == [-8.0,0.0,-8.0] and [self.size_x,self.size_y,self.size_z] == [16.0,16.0,16.0]:
            return True
        return {
            "origin":[self.origin_x,self.origin_y,self.origin_z],
            "size":[self.size_x,self.size_y,self.size_z]
        }

    def getUiDict(self):
        if not self.enable:
            return {"enable":(self.enable,"bool",None)}
        return {
            "enable": (self.enable,"bool",None),
            "origin": {
                "x": (self.origin_x,"float",(-8,8)),
                "y": (self.origin_y,"float",(0,16)),
                "z": (self.origin_z,"float",(-8,8))
            },
            "size": {
                "x": (self.size_x,"float",(-8,8)),
                "y": (self.size_y,"float",(0,16)),
                "z": (self.size_z,"float",(-8,8))
            }
        }

    def write(self,pack_dict):
        pack_dict["minecraft:block"]["components"][self.identifier] = self.generate()

    def parseFromUi(self,ui_dict):
        self.enable = lib.getWidgetValue(ui_dict["enable"])

        if "origin" in ui_dict:
            self.origin_x = lib.getWidgetValue(ui_dict["origin"]["x"])
            self.origin_y = lib.getWidgetValue(ui_dict["origin"]["y"])
            self.origin_z = lib.getWidgetValue(ui_dict["origin"]["z"])
        if "size" in ui_dict:
            self.size_x = lib.getWidgetValue(ui_dict["size"]["x"])
            self.size_y = lib.getWidgetValue(ui_dict["size"]["y"])
            self.size_z = lib.getWidgetValue(ui_dict["size"]["z"])
            if self.origin_x+self.size_x > 8:
                self.size_x = 8-self.origin_x
            if self.origin_y+self.size_y > 16:
                self.size_y = 16-self.origin_y
            if self.origin_z+self.size_z > 8:
                self.size_z = 8-self.origin_z
            if self.origin_x+self.size_x < -8:
                self.size_x = -8-self.origin_x
            if self.origin_y+self.size_y < 0:
                self.size_y = -self.origin_y
            if self.origin_z+self.size_z < -8:
                self.size_z = -8-self.origin_z


components = {"minecraft:collision_box":CollisionBox}
