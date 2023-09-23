import os, json, uiSystem
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog


def buildDirectories(path, directories):
    p = os.getcwd()
    os.chdir(path)
    for directory in directories:
        if directory not in os.listdir():
            os.mkdir(directory)
        buildDirectories(directory, directories[directory])
    os.chdir(p)


def getBedrockGameVersionsList():
    with open("./data/versions.json", "r") as f:
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
    if isinstance(widget, QtWidgets.QCheckBox) and not widget.isTristate():  # bool
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
    if isinstance(widget, QtWidgets.QCheckBox) and widget.isTristate():  # tristate
        state = widget.checkState()
        if state == Qt.Unchecked:
            return 0
        if state == Qt.PartiallyChecked:
            return 1
        return 2
    if isinstance(widget, ListEditButton):
        return widget.list_


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
            for key, value in readDataFromFile(f"lang/{id}/{file}"):
                self.lang[f"{file.replace('.lang','')}_{key}"] = value
        self.lang_keys = self.lang.keys()

    def __getitem__(self, t):
        module, lang_id = t
        if f"{module}_{lang_id}" in self.lang_keys:
            return self.lang[f"{module}_{lang_id}"]
        return f"{module}_{lang_id}"


def clearLayout(layout):
    item_list = list(range(layout.count()))
    item_list.reverse()

    for i in item_list:
        item = layout.itemAt(i)
        layout.removeItem(item)
        if item.widget():
            item.widget().deleteLater()
        else:
            clearLayout(item)


class Dialog(QDialog):
    def __init__(self, parent, dialog_list, dialog_ui_list):
        self.dialog_list = dialog_list
        self.dialog_ui_list = dialog_ui_list
        super(Dialog, self).__init__(parent)

    def close(self) -> bool:
        index = self.dialog_list.index(self)
        self.dialog_list.pop(index)
        self.dialog_ui_list.pop(index)
        return super(Dialog, self).close()


def readDataFromFile(filename):
    with open(filename, "r", encoding="utf-8") as f:
        for line in f.readlines():
            if line.find("=") == -1:
                continue
            index = line.find("//")
            if index != -1:
                line = line[:index]
            if line[-1] == "\n":
                line = line[:-1]
            key, value = line.split("=")
            yield key, value


class ListEditButton(QtWidgets.QPushButton):
    def __init__(self, parent):
        super(ListEditButton, self).__init__(parent)
        self.list_ = []

    def bind(self, callback):
        self.clicked.connect(lambda: uiSystem.AskList("List", self.list_, callback))


class LockHorizontalScrollArea(QtWidgets.QScrollArea):
    def resizeEvent(self, a0: QtGui.QResizeEvent) -> None:
        self.widget().setGeometry(
            0, 0, a0.size().width(), self.widget().size().height()
        )
