import uiSystem, addon, lib, sys, json
from zipfile import ZipFile
from os import mkdir,listdir
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5 import QtGui

class MainSystem:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.app.setWindowIcon(QtGui.QIcon("./resources/ico.ico"))
        self.ui = None
        self.project_object = None
        self.lang = lib.Language("en-us")
        self.config = {}

    def load(self):
        self.loadConfig()
        self.bedrock_game_version_list = lib.getBedrockGameVersionsList()
        self.loadLanguage(self.config["lang"])

    def loadLanguage(self,lang):
        self.lang.loadLangFolder(lang)

    def run(self):
        self.ui = uiSystem.UiSystem(self)
        self.ui.show()
        self.app.exec_()

    def askOpenProject(self):
        file = QFileDialog.getOpenFileName(self.ui)[0]
        if file == "":
            return
        self.openProject(file)

    def openProject(self,file):
        zip = ZipFile(file, "r")
        zip.extractall("./tmp")
        dir_name = zip.namelist()[0].split("/")[0]
        path = f"./tmp/{dir_name}"
        zip.close()
        with open(f"{path}/project.json","r") as f:
            project_data = json.load(f)
        if project_data["pack_type"] == "addon":
            self.project_object = addon.BedrockAddon(self)
            self.project_object.save_path = file
            self.project_object.load(path,project_data)
            self.ui.changeUi(uiSystem.AddonUi())
        else:
            QMessageBox.critical(self.ui,self.lang["ui","error"],self.lang["ui","unsupported_project"])

    def loadConfig(self):
        self.config = {}
        with open("config","r") as f:
            for line in f.readlines():
                line = line[:-1]
                key,value = line.split("=")
                self.config[key] = value

# Init
if "tmp" not in listdir():
    mkdir("tmp")
if "config" not in listdir():
    with open("config","w") as f:
        f.write("lang=en-us\ntheme=Default\n")

main = MainSystem()
main.load()
main.run()
with open("config", "w") as f:
    for key in main.config:
        f.write(f"{key}={main.config[key]}\n")
