class BasicComponent:
    def __init__(self, identifier, content, ui_system):
        self.identifier = identifier
        self.content = content
        self.ui_system = ui_system

    def parse(self, component_value):
        pass

    def generate(self):
        pass

    def write(self, pack_dict):
        pass

    def getUiDict(self):
        pass

    def parseFromUi(self):
        pass
