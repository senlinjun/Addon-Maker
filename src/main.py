import uiSystem, addon, lib, sys, json
from zipfile import ZipFile
from os import mkdir, listdir
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import Qt

from uiSystem import AskList, AddonSetting


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

    def loadLanguage(self, lang):
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

    def openProject(self, file):
        lib.clearFolder("tmp")
        zip = ZipFile(file, "r")
        zip.extractall("./tmp")
        dir_name = zip.namelist()[0].split("/")[0]
        path = f"./tmp/{dir_name}"
        zip.close()
        with open(f"{path}/project.json", "r") as f:
            project_data = json.load(f)
        if project_data["pack_type"] == "addon":
            self.project_object = addon.BedrockAddon(self)
            self.project_object.save_path = file
            self.project_object.load(path, project_data)
            self.ui.changeUi(uiSystem.AddonUi())
        else:
            QMessageBox.critical(
                self.ui,
                self.lang["ui", "error"],
                self.lang["ui", "unsupported_project"],
            )

    def loadConfig(self):
        self.config = {}
        for key, value in lib.readDataFromFile("config"):
            self.config[key] = value

    def setDataUi(
        self,
        group_box,
        form_layout,
        data_dict: dict,
        component_identifier: str,
        component_type: str,
        changed_callback,
    ):
        size = 30  # groupBox所占的30px
        count = 0
        data_ui_dict = {}
        for key in data_dict:
            label = QtWidgets.QLabel(group_box)
            label.setObjectName("label")
            label.setText(key)
            form_layout.setWidget(count, QtWidgets.QFormLayout.LabelRole, label)
            child = None

            field = None
            if isinstance(data_dict[key], dict):
                new_group_box = QtWidgets.QGroupBox(group_box)
                new_group_box.setObjectName("groupBox")
                new_group_box.setTitle(key)
                new_form_layout = QtWidgets.QFormLayout(new_group_box)
                new_form_layout.setObjectName("formLayout")
                child, child_size = self.setDataUi(
                    new_group_box,
                    new_form_layout,
                    data_dict[key],
                    component_identifier,
                    component_type,
                    changed_callback,
                )
                field = new_group_box
                size += child_size

            else:
                value, value_type, args = data_dict[key]

                if value_type == "bool":
                    field = QtWidgets.QCheckBox(group_box)
                    field.setObjectName("checkBox")
                    field.setChecked(value)
                    field.stateChanged.connect(
                        lambda: changed_callback("widget", item=field)
                    )

                elif value_type == "int":
                    field = QtWidgets.QSpinBox(group_box)
                    field.setObjectName("spinBox")
                    if args is not None:
                        field.setMinimum(args[0])
                        field.setMaximum(args[1])
                        if len(args) >= 3:
                            field.setSingleStep(args[2])
                    field.setValue(value)
                    field.valueChanged.connect(
                        lambda: changed_callback("widget", item=field)
                    )

                elif value_type == "float":
                    field = QtWidgets.QDoubleSpinBox(group_box)
                    field.setObjectName("doubleSpinBox")
                    if args is not None:
                        field.setMinimum(args[0])
                        field.setMaximum(args[1])
                        if len(args) >= 3:
                            field.setSingleStep(args[2])
                    field.setValue(value)
                    field.valueChanged.connect(
                        lambda: changed_callback("widget", item=field)
                    )

                elif value_type == "str":
                    field = QtWidgets.QLineEdit(group_box)
                    field.setObjectName("lineEdit")
                    if args is not None:
                        field.setMaxLength(args)
                    field.setText(value)
                    field.textChanged.connect(
                        lambda: changed_callback("widget", item=field)
                    )

                elif value_type == "combobox":
                    if args is not None:
                        field = QtWidgets.QComboBox(group_box)
                        field.setObjectName("comboBox")
                        field.addItems(args)
                        field.setCurrentText(value)
                        field.currentIndexChanged.connect(
                            lambda: changed_callback(field)
                        )

                elif value_type == "button":
                    field = QtWidgets.QPushButton(group_box)
                    field.setObjectName("pushButton")
                    field.setText(args)
                    field.clicked.connect(value)

                elif value_type == "list":
                    field = QtWidgets.QPushButton(group_box)
                    field.setObjectName("pushButton")
                    field.setText(self.lang["ui", "edit"])
                    field.component_list = value
                    k = key
                    field.clicked.connect(
                        lambda: self.editList(k, value, changed_callback)
                    )

                elif value_type == "tristate":
                    field = QtWidgets.QCheckBox(group_box)
                    field.setObjectName("checkBox")
                    field.setTristate()
                    if value == 0:
                        field.setCheckState(Qt.Unchecked)
                    elif value == 1:
                        field.setCheckState(Qt.PartiallyChecked)
                    elif value == 2:
                        field.setCheckState(Qt.Checked)
                    field.stateChanged.connect(
                        lambda: changed_callback("widget", item=field)
                    )

                if field is None:
                    field = QtWidgets.QLabel(group_box)
                    field.setObjectName("label")
                    field.setText(
                        f'{self.lang["ui", "unsupported_type"]}({value_type})'
                    )

            field.identifier = component_identifier
            field.type = component_type
            form_layout.setWidget(count, QtWidgets.QFormLayout.FieldRole, field)
            if child is None:
                data_ui_dict[key] = field
            else:
                data_ui_dict[key] = child
            count += 1
            size += 25
        return data_ui_dict, size

    def editList(self, list_name, list_, callback_func):
        self.ui.showDialog(AskList(list_name, list_, callback_func))


# Init
if "tmp" not in listdir():
    mkdir("tmp")
if "config" not in listdir():
    with open("config", "w") as f:
        f.write("lang=en-us\ntheme=Default\n")

argv = sys.argv
main = MainSystem()
main.load()
main.run()
with open("config", "w") as f:
    for key in main.config:
        f.write(f"{key}={main.config[key]}\n")
