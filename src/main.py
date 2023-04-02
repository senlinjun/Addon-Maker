import uiSystem, addon, lib, sys, os
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtGui

class MainSystem:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setWindowIcon(QtGui.QIcon("./resources/ico.ico"))
        self.ui = uiSystem.UiSystem(self)
        self.project_object = None

    def load(self):
        self.bedrock_game_version_list = lib.getBedrockGameVersionsList()

    def run(self):
        self.ui.show()
        self.app.exec_()


# Init
if "works" not in os.listdir():
    os.mkdir("works")

main = MainSystem()
main.load()
main.run()
