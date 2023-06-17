class BasicComponent:
    def __init__(self,identifier,content):
        self.identifier = identifier
        self.content = content

    def parse(self,component_value):
        pass

    def generate(self):
        pass

    def write(self,pack_dict):
        pass

    def getUiDict(self):
        pass

    def parseFromUi(self):
        pass
