import uiSystem, addon, lib, sys
from PyQt5.QtWidgets import QApplication

class MainSystem:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.ui = uiSystem.UiSystem(self)
        self.project_object = None

    def load(self):
        self.bedrock_game_version_list = lib.getBedrockGameVersionsList()

    def run(self):
        self.ui.show()
        self.app.exec_()


main = MainSystem()
main.load()
main.run()
