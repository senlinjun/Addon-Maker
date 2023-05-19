import os
import random, lib, sys, addon, os, json

from ui import start,addonUi,addon_setting
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QInputDialog, QDialog
from PyQt5.QtCore import QCoreApplication

'''
每个ui都必须有
init()方法
close_callback布尔值变量
close()方法（如果close_callback为True）
'''
class UiBasic:
    def __init__(self):
        self.close_callback = False

    def close(self):
        pass

    def init(self):
        pass

class StartUi(start.Ui_MainWindow,UiBasic):

    def setupUi(self, uiSystem):
        super().setupUi(uiSystem)
        self.uiSystem = uiSystem

    def init(self):
        self.rename()
        self.bind()
        img = QtGui.QPixmap("./resources/start.png")
        self.img.setPixmap(img)

    def rename(self):
        _translate = QtCore.QCoreApplication.translate
        self.uiSystem.setWindowTitle(_translate("Form", "Start"))
        self.new_addon.setText(_translate("Form", "New Bedrock Addon"))
        self.new_mod.setText(_translate("Form", "New Java Mod"))
        self.open.setText(_translate("Form", "Open"))
        self.setting.setText(_translate("Form", "setting"))

    def bind(self):
        self.new_addon.clicked.connect(self.addonClicked)
        self.open.clicked.connect(self.uiSystem.MainSystem.askOpenProject)

    def addonClicked(self):
        self.uiSystem.changeUi(AddonSetting(self))


class AddonUi(addonUi.Ui_MainWindow, UiBasic):
    def setupUi(self, uiSystem):
        super().setupUi(uiSystem)
        self.uiSystem = uiSystem

    def init(self):
        self.component_data = {}
        self.close_callback = True
        self.rename()
        self.bind()
        self.updateComponentList()

    def rename(self):
        _translate = QtCore.QCoreApplication.translate
        self.uiSystem.setWindowTitle(_translate("MainWindow", f"Addon({self.uiSystem.MainSystem.project_object.packname})"))
        self.component_tab.setTabText(self.component_tab.indexOf(self.all), _translate("MainWindow", "All"))
        self.component_tab.setTabText(self.component_tab.indexOf(self.block), _translate("MainWindow", "Block"))
        self.component_tab.setTabText(self.component_tab.indexOf(self.item), _translate("MainWindow", "Item"))
        self.component_tab.setTabText(self.component_tab.indexOf(self.entity), _translate("MainWindow", "Entity"))
        self.component_tab.setTabText(self.component_tab.indexOf(self.feature), _translate("MainWindow", "Feature"))
        self.component_tab.setTabText(self.component_tab.indexOf(self.recipe), _translate("MainWindow", "Recipe"))

    def updateComponentList(self):
        self.all_list.clear()
        self.block_list.clear()
        self.item_list.clear()
        self.entity_list.clear()
        self.feature_list.clear()
        self.recipe_list.clear()

        # blocks
        blocks_identifier = [key for key in self.uiSystem.MainSystem.project_object.blocks]
        blocks_identifier.sort()
        self.all_list.addItems([f"[BLOCK] {identifier}" for identifier in blocks_identifier])
        self.block_list.addItems([f"[BLOCK] {identifier}" for identifier in blocks_identifier])

    def bind(self):
        self.addItem.clicked.connect(self.addComponent)
        self.removeItem.clicked.connect(self.removeComponent)
        self.actionSave.triggered.connect(self.save)
        self.actionOpen.triggered.connect(self.uiSystem.MainSystem.askOpenProject)
        self.actionBedrock_Addon.triggered.connect(lambda:self.uiSystem.changeUi(AddonSetting(self)))
        self.actionExport.triggered.connect(self.export)
        self.all_list.itemClicked.connect(self.updateComponentData)

    def addComponent(self):
        current_text = self.component_tab.tabText(self.component_tab.currentIndex())
        if current_text == "All":
            select = QInputDialog.getItem(self.uiSystem,"addComponent","Select the component you want to add",["Block","Item","Entity","Feature","Recipe"],current=0,editable=False)
            if not select[1]:
                return
            item = select[0]
            if item == "Block":
                self.addComponentBlock()
        elif current_text == "Block":
            self.addComponentBlock()

    def addComponentBlock(self):
        new_block_input = QInputDialog.getText(self.uiSystem,"newBlock",'Enter the identifier of the New Block(example:"abc:apple")',text=f"{self.uiSystem.MainSystem.project_object.namespace}:",)
        if not new_block_input[1]:
            return
        identifier = new_block_input[0]
        if identifier.find(" ") != -1:
            QMessageBox.critical(self.uiSystem, "error", "Cannot contain Spaces")
            return
        namespace,id = identifier.split(":")

        new_block = addon.Block(self.uiSystem.MainSystem.project_object)
        new_block.new(namespace,id)
        self.uiSystem.MainSystem.project_object.blocks[new_block.identifier] = new_block
        self.updateComponentList()

    def removeComponent(self):
        return_back = self.getSelectComponent()
        if return_back == None:
            return
        component_type, component = return_back
        component.remove()
        self.updateComponentList()

    def getSelectComponent(self):
        """
        :return:
        (type,component)/None
        """
        tab_index = self.component_tab.currentIndex()
        components_dict = {0:self.all_list,1:self.block_list,2:self.item_list,3:self.entity_list,4:self.feature_list,5:self.recipe_list}
        component = components_dict[tab_index].currentItem()
        if component is None:
            return None
        component_text = component.text()
        component_type,component_identifier = component_text.split(" ")
        if component_type == "[BLOCK]":
            return component_type, self.uiSystem.MainSystem.project_object.blocks[component_identifier]

    def save(self):
        if self.uiSystem.MainSystem.project_object.save_path is None:
            save_path = QFileDialog.getSaveFileName(self.uiSystem,filter="'amproject(*.amproject)'")[0]
            if save_path == "":
                return
            self.uiSystem.MainSystem.project_object.save_path = save_path
        self.uiSystem.MainSystem.project_object.save()

    def export(self):
        path = QFileDialog.getExistingDirectory(self.uiSystem)
        if path == "":
            return
        self.uiSystem.MainSystem.project_object.export(path)

    def close(self):
        self.uiSystem.MainSystem.project_object.close()
        QCoreApplication.instance().quit()

    def updateComponentData(self):
        self.clearLayout(self.behavior_layout)
        self.clearLayout(self.resource_layout)
        component = self.getSelectComponent()
        if component is None:
            return
        component_type,component = component
        for component_data_obj in component.components:
            group_box = QtWidgets.QGroupBox(self.behavior_scrollAreaWidgetContents)
            group_box.setObjectName("groupBox")
            form_layout = QtWidgets.QFormLayout(group_box)
            form_layout.setObjectName("formLayout")
            self.setComponentDataUi(group_box,form_layout,component_data_obj.getUiDict())
            self.behavior_layout.addWidget(group_box)

    def setComponentDataUi(self,group_box,form_layout,data_dict:dict):
        count = 0
        for key in data_dict:
            label = QtWidgets.QLabel(group_box)
            label.setObjectName("label")
            label.setText(key)
            form_layout.setWidget(count, QtWidgets.QFormLayout.LabelRole,label)

            value = data_dict[key]
            field = None
            if isinstance(value,dict):
                new_group_box = QtWidgets.QGroupBox(group_box)
                new_group_box.setObjectName("groupBox")
                new_group_box.setTitle(key)
                new_form_layout = QtWidgets.QFormLayout(new_group_box)
                new_form_layout.setObjectName("formLayout")
                self.setComponentDataUi(new_group_box,new_form_layout,value)
                field = new_group_box

            elif isinstance(value,bool):
                field = QtWidgets.QCheckBox(group_box)
                field.setObjectName("checkBox")
                field.setChecked(value)

            elif isinstance(value,int):
                field = QtWidgets.QSpinBox(group_box)
                field.setObjectName("spinBox")
                field.setValue(value)

            elif isinstance(value,float):
                field = QtWidgets.QDoubleSpinBox(group_box)
                field.setObjectName("doubleSpinBox")
                field.setValue(value)

            elif isinstance(value,str):
                field = QtWidgets.QLineEdit(group_box)
                field.setObjectName("lineEdit")
                field.setText(value)

            if field is None:
                field = QtWidgets.QLabel(group_box)
                field.setObjectName("label")
                field.setText("Unsupported data type")
            form_layout.setWidget(count, QtWidgets.QFormLayout.FieldRole,field)
            count += 1

    def clearLayout(self, layout):
        item_list = list(range(layout.count()))
        item_list.reverse()

        for i in item_list:
            item = layout.itemAt(i)
            layout.removeItem(item)
            if item.widget():
                item.widget().deleteLater()
            else:
                self.clearLayout(item)


class AddonSetting(addon_setting.Ui_MainWindow,UiBasic):
    def __init__(self,last_ui):
        super().__init__()
        self.last_ui = last_ui

    def setupUi(self, uiSystem):
        super().setupUi(uiSystem)
        self.uiSystem = uiSystem

    def init(self):
        self.icon_path = "resources/test.png"
        self.rename()
        self.bind()
        self.close_callback = True
        self.choose_main_version.addItems(self.uiSystem.MainSystem.bedrock_game_version_list.keys())
        self.choose_main_version.setCurrentIndex(0)
        self.icon.setPixmap(QtGui.QPixmap(self.icon_path))

    def bind(self):
        self.Cancel.clicked.connect(lambda:self.uiSystem.changeUi(self.last_ui))
        self.random_namepace.clicked.connect(self.randomNamespace)
        self.choose_main_version.currentTextChanged.connect(self.mainVersionChanged)
        self.choose_icon.clicked.connect(self.chooseIcon)
        self.Ok.clicked.connect(self.OK)

    def rename(self):
        _translate = QtCore.QCoreApplication.translate
        self.uiSystem.setWindowTitle(_translate("MainWindow", "Setting Addon"))
        self.description_label_2.setText(_translate("MainWindow", "description"))
        self.namespace_label.setText(_translate("MainWindow", "namespace"))
        self.random_namepace.setText(_translate("MainWindow", "random"))
        self.packName_label.setText(_translate("MainWindow", "Packname"))
        self.pack_version_label.setText(_translate("MainWindow", "pack_version"))
        self.label_4.setText(_translate("MainWindow", "."))
        self.label_3.setText(_translate("MainWindow", "."))
        self.game_version_label.setText(_translate("MainWindow", "game_minimum_version"))
        self.icon_label.setText(_translate("MainWindow", "pack_icon"))
        self.icon.setText(_translate("MainWindow", "<html><head/><body><p>Img</p><p><br/></p></body></html>"))
        self.choose_icon.setText(_translate("MainWindow", "choose"))
        self.Ok.setText(_translate("MainWindow", "Ok"))
        self.Cancel.setText(_translate("MainWindow", "Cancel"))

    def mainVersionChanged(self):
        self.choose_detailed_version.clear()
        self.choose_detailed_version.addItems(self.uiSystem.MainSystem.bedrock_game_version_list[self.choose_main_version.currentText()])
        self.choose_detailed_version.setCurrentIndex(0)

    def close(self):
        self.uiSystem.changeUi(self.last_ui)

    def randomNamespace(self):
        namespace = ""
        for i in range(5):
            namespace += chr(random.randint(97,97+26-1))
        self.namespace_2.setText(namespace)

    def chooseIcon(self):
        path = QFileDialog.getOpenFileName(self.uiSystem)
        if path[0] != "":
            self.icon_path = path[0]
            self.icon.setPixmap(QtGui.QPixmap(self.icon_path))

    def OK(self):
        if self.check():
            self.uiSystem.MainSystem.project_object = addon.BedrockAddon(self.uiSystem.MainSystem)
            self.uiSystem.MainSystem.project_object.new(
                "./tmp",
                2,
                self.packName.text(),
                self.description.toPlainText(),
                self.namespace_2.text(),
                [int(self.pack_version_0.text()),int(self.pack_version_1.text()),int(self.pack_version_2.text())],
                [int(number) for number in self.choose_detailed_version.currentText().split(".")]
            )
            self.uiSystem.MainSystem.project_object.setPackIcon(self.icon_path)
            self.uiSystem.changeUi(AddonUi())

    def check(self):
        blank = []
        if self.packName.text() == "":
            blank.append("PackName")
        if self.namespace_2.text() == "":
            blank.append("Namespace")
        if blank == []:
            return True

        message = f"Do not leave blank!\n("
        for name in blank:
            message += name
            message += ','
        message = message[:-1]+')'
        QMessageBox.critical(self.uiSystem, "error", message)
        return False


class UiSystem(QMainWindow):
    def __init__(self,MainSystem,Ui=StartUi()):
        super().__init__()
        self.MainSystem = MainSystem
        self.ui = None
        self.changeUi(Ui)

    def changeUi(self,ui_obj):
        self.ui = ui_obj
        self.ui.setupUi(self)
        self.ui.init()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.ui.close_callback:
            event.ignore()
            self.ui.close()


class AskComponents:
    def __init__(self,dialog,component_dict,callback_func):
        self.dialog = dialog
        self.component_dict = component_dict
        self.callback_func = callback_func
        self.component_enable_ui = {}

    def setupUi(self):
        Dialog = self.dialog
        Dialog.setObjectName("Dialog")
        Dialog.setEnabled(True)
        Dialog.resize(670, 430)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.search = QtWidgets.QLineEdit(Dialog)
        self.search.setObjectName("search")
        self.verticalLayout.addWidget(self.search)
        self.scrollArea = QtWidgets.QScrollArea(Dialog)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setWidgetResizable(False)
        self.scrollArea.setObjectName("scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 650, 120))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.scrollAreaWidgetContents_2 = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents_2.setObjectName("scrollAreaWidgetContents_2")
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.bottom = QtWidgets.QHBoxLayout()
        self.bottom.setObjectName("bottom")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.bottom.addItem(spacerItem)
        self.DialogButtonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.DialogButtonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.DialogButtonBox.setObjectName("DialogButtonBox")
        self.bottom.addWidget(self.DialogButtonBox)
        self.verticalLayout.addLayout(self.bottom)

        self.rename()
        self.showComponents()
        self.bind()

    def showComponents(self):
        component_dict = self.component_dict
        self.component_enable_ui = {}
        for component_identifier in component_dict:
            component_info = component_dict[component_identifier]
            component_layout = QtWidgets.QHBoxLayout()
            component_layout.setObjectName("component_layout")
            text = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            text.setObjectName("text")
            component_layout.addWidget(text)
            identifier = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            identifier.setObjectName("identifier")
            component_layout.addWidget(identifier)
            description = QtWidgets.QTextBrowser(self.scrollAreaWidgetContents)
            description.setObjectName("description")
            component_layout.addWidget(description)
            enable = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
            enable.setObjectName("enable")
            component_layout.addWidget(enable)
            self.scrollAreaWidgetContents_2.addLayout(component_layout)

            text.setText(component_info["name"])
            identifier.setText(component_identifier)
            description.setText(component_info["description"])
            enable.setChecked(component_info["is_checked"])

            self.component_enable_ui[component_identifier] = enable

    def rename(self):
        self.dialog.setWindowTitle("components")
        self.search.setPlaceholderText("search")

    def bind(self):
        self.DialogButtonBox.rejected.connect(self.dialog.close)
        self.DialogButtonBox.accepted.connect(self.ok)

    def ok(self):
        component_enable = {}
        for identifier in self.component_dict:
            component_enable[identifier] = self.component_enable_ui[identifier].isChecked()
        self.callback_func(component_enable)
        self.dialog.close()
