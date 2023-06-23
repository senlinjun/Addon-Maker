import os,json
from PyQt5 import QtWidgets


def buildDirectories(path, directories):
    p = os.getcwd()
    os.chdir(path)
    for directory in directories:
        if directory not in os.listdir():
            os.mkdir(directory)
        buildDirectories(directory, directories[directory])
    os.chdir(p)


def getBedrockGameVersionsList():
    with open("./data/versions.json","r") as f:
        return_dict = json.load(f)
    return return_dict


def clearFolder(folder_path):
    path = os.getcwd()
    os.chdir(folder_path)
    for filename in os.listdir():
        if os.path.isdir(filename):
            clearFolder(filename)
            os.removedirs(filename)
        else:
            os.remove(filename)
    os.chdir(path)


def compressDir(dir_path, zip_obj, prefix=""):
    for file in os.listdir(dir_path):
        if os.path.isdir(f"{dir_path}/{file}"):
            compressDir(f"{dir_path}/{file}", zip_obj, f"{prefix}/{file}")
        else:
            zip_obj.write(f"{dir_path}/{file}", f"{prefix}/{file}")


def getWidgetValue(widget):
    if isinstance(widget, QtWidgets.QCheckBox):  # bool
        return widget.isChecked()
    if isinstance(widget, QtWidgets.QSpinBox):  # int
        return widget.value()
    if isinstance(widget, QtWidgets.QDoubleSpinBox):  # float
        return widget.value()
    if isinstance(widget, QtWidgets.QLineEdit):  # str
        return widget.text()
    if isinstance(widget, QtWidgets.QTextEdit):  # str
        return widget.toPlainText()
    if isinstance(widget, QtWidgets.QComboBox):  # list(comboBox)
        return widget.currentText()


class Language:
    def __init__(self, id):
        self.lang = {}
        self.lang_info = {}
        self.lang_keys = []
        self.loadLangFolder(id)

    def loadLangFolder(self, id):
        self.lang = {}
        self.lang_info = {}
        self.id = id
        for file in os.listdir(f"lang/{id}"):
            if file == "language":
                with open(f"lang/{id}/language", "r", encoding="utf-8") as f:
                    for line in f.readlines():
                        line = line[:-1]
                        key, value = line.split("=")
                        self.lang_info[key] = value

            with open(f"lang/{id}/{file}", "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if "=" not in line:
                        continue
                    if line[-1] == "\n":
                        line = line[:-1]
                    key, value = line.split("=")
                    self.lang[f"{file.replace('.lang','')}_{key}"] = value
        self.lang_keys = self.lang.keys()

    def __getitem__(self, t):
        module, lang_id = t
        if f"{module}_{lang_id}" in self.lang_keys:
            return self.lang[f"{module}_{lang_id}"]
        return f"{module}_{lang_id}"
