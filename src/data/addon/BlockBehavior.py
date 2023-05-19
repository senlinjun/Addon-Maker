from data.addon.basic_component import BasicComponent

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
            return {"enable":self.enable}
        return {
            "enable": self.enable,
            "origin": {
                "x": self.origin_x,
                "y": self.origin_y,
                "z": self.origin_z
            },
            "size": {
                "x": self.size_x,
                "y": self.size_y,
                "z": self.size_z
            }
        }

    def write(self,pack_dict):
        pack_dict["minecraft:block"]["components"][self.identifier] = self.generate()


components = {"minecraft:collision_box":CollisionBox}
