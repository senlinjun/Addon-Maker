import uiSystem, addon, lib, sys, os, json, zipfile
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
        file = QFileDialog.getOpenFileName(self.ui)[0]
        if file == "":
            return
        self.openProject(file)

    def openProject(self,file):
        zip = zipfile.ZipFile(file, "r")
        zip.extractall("./tmp")
        dir_name = zip.namelist()[0].split("/")[0]
        path = f"./tmp/{dir_name}"
        zip.close()
        with open(f"{path}/project.json","r") as f:
            project_data = json.load(f)
        if project_data["pack_type"] == "addon":
            self.project_object = addon.BedrockAddon()
            self.project_object.save_path = file
            self.project_object.load(path,project_data)
            self.ui.changeUi(uiSystem.AddonUi())
        else:
            QMessageBox.critical(self.ui,"error","We can't open this project.\n(Unsupported project)")
        lib.clearFolder("tmp")

# Init
if "tmp" not in os.listdir():
    os.mkdir("tmp")

main = MainSystem()
main.load()
main.run()