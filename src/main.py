import uiSystem, addon, lib, sys, os, json
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
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

    def askOpenProject(self):
        path = QFileDialog.getExistingDirectory(self.ui)
        if path == "":
            return

        if "project.json" in os.listdir(path):
            self.openProject(path)
        else:
            QMessageBox.critical(self.ui,"error","Not an Addon Maker project")

    def openProject(self,path):
        with open(f"{path}/project.json","r") as f:
            project_data = json.load(f)
        if project_data["pack_type"] == "addon":
            self.project_object = addon.BedrockAddon()
            self.project_object.load(path,project_data)
            self.ui.changeUi(uiSystem.AddonUi())
        else:
            QMessageBox.critical(self.ui,"error","We can't open this project.\n(Unsupported project)")

# Init
if "works" not in os.listdir():
    os.mkdir("works")

main = MainSystem()
main.load()
main.run()
