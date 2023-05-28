import os
import random, lib, sys, addon, os, json

from ui import start,addonUi,addon_setting,ask_components,setting
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox, QInputDialog, QDialog, QAbstractItemView
from PyQt5.QtCore import QCoreApplication, Qt

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
        self.uiSystem.setWindowTitle("Start")
        self.new_addon.setText("New Bedrock Addon")
        self.new_mod.setText("New Java Mod")
        self.open.setText("Open")
        self.setting.setText("setting")

    def bind(self):
        self.new_addon.clicked.connect(self.addonClicked)
        self.open.clicked.connect(self.uiSystem.MainSystem.askOpenProject)
        self.setting.clicked.connect(lambda:self.uiSystem.showDialog(Setting()))

    def addonClicked(self):
        self.uiSystem.changeUi(AddonSetting(self))


class AddonUi(addonUi.Ui_MainWindow, UiBasic):
    def setupUi(self, uiSystem):
        super().setupUi(uiSystem)
        self.uiSystem = uiSystem

    def init(self):
        self.component_ui = {}
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
        self.modifyComponents.clicked.connect(self.clickedModifyComponent)

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
        self.component_ui = {}
        component_type,component = component
        for component_identifier in component.components:
            component_data_obj = component.components[component_identifier]
            ui_dict = component_data_obj.getUiDict()
            group_box = QtWidgets.QGroupBox(self.behavior_scrollAreaWidgetContents)
            group_box.setObjectName("groupBox")
            form_layout = QtWidgets.QFormLayout(group_box)
            form_layout.setObjectName("formLayout")
            self.component_ui[component_identifier] = self.setComponentDataUi(group_box, form_layout, ui_dict, component_data_obj.identifier)
            self.behavior_layout.addWidget(group_box)

    def setComponentDataUi(self,group_box,form_layout,data_dict:dict,component_identifier:str):
        count = 0
        data_ui_dict = {}
        for key in data_dict:
            label = QtWidgets.QLabel(group_box)
            label.setObjectName("label")
            label.setText(key)
            form_layout.setWidget(count, QtWidgets.QFormLayout.LabelRole,label)
            child = None

            field = None
            if isinstance(data_dict[key],dict):
                new_group_box = QtWidgets.QGroupBox(group_box)
                new_group_box.setObjectName("groupBox")
                new_group_box.setTitle(key)
                new_form_layout = QtWidgets.QFormLayout(new_group_box)
                new_form_layout.setObjectName("formLayout")
                child = self.setComponentDataUi(new_group_box,new_form_layout,data_dict[key],component_identifier)
                field = new_group_box

            value, value_type, value_limit = data_dict[key]

            if value_type == "bool":
                field = QtWidgets.QCheckBox(group_box)
                field.setObjectName("checkBox")
                field.setChecked(value)
                field.stateChanged.connect(lambda:self.componentDataChanged(field))

            elif value_type == "int":
                field = QtWidgets.QSpinBox(group_box)
                field.setObjectName("spinBox")
                if value_limit is not None:
                    field.setMinimum(value_limit[0])
                    field.setMaximum(value_limit[1])
                field.setValue(value)
                field.valueChanged.connect(lambda:self.componentDataChanged(field))

            elif value_type == "float":
                field = QtWidgets.QDoubleSpinBox(group_box)
                field.setObjectName("doubleSpinBox")
                if value_limit is not None:
                    field.setMinimum(value_limit[0])
                    field.setMaximum(value_limit[1])
                field.setValue(value)
                field.valueChanged.connect(lambda:self.componentDataChanged(field))

            elif value_type == "str":
                field = QtWidgets.QLineEdit(group_box)
                field.setObjectName("lineEdit")
                if value_limit is not None:
                    field.setMaxLength(value_limit)
                field.setText(value)
                field.textChanged.connect(lambda:self.componentDataChanged(field))

            if field is None:
                field = QtWidgets.QLabel(group_box)
                field.setObjectName("label")
                field.setText("Unsupported data type")

            field.identifier = component_identifier
            form_layout.setWidget(count, QtWidgets.QFormLayout.FieldRole,field)
            if child is None:
                data_ui_dict[key] = field
            else:
                data_ui_dict[key] = child
            count += 1
        return data_ui_dict

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

    def componentDataChanged(self,item):
        ui_dict = self.component_ui[item.identifier]
        component_obj = self.getSelectComponent()
        if component_obj is None:
            return
        component_data_obj = component_obj[1].components[item.identifier]
        component_data_obj.parseFromUi(ui_dict)
        self.updateComponentData()

    def clickedModifyComponent(self):
        component = self.getSelectComponent()
        if component is None:
            return
        component_type,component = component

        dialog = AskComponent(component.getBehaviorComponents(),self.modifyComponentCallback)
        self.uiSystem.showDialog(dialog)
        dialog.showComponents()

    def modifyComponentCallback(self,component_dict):
        component = self.getSelectComponent()
        if component is None:
            return
        component_type, component = component
        for component_data in component_dict:
            print(component.components,component_dict[component_data],component)
            if component_data in component.components and not component_dict[component_data]:
                component.components.pop(component_data)
            elif component_data not in component.components and component_dict[component_data]:
                component.addBehaviorComponent(component_data)
        self.updateComponentData()


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


class AskComponent(ask_components.Ui_Dialog,UiBasic):
    def __init__(self, component_dict, callback_func):
        super().__init__()
        self.component_dict = component_dict
        self.callback_func = callback_func

    def showComponents(self,component_dict=None):
        if component_dict is None:
            component_dict = self.component_dict

        self.tableWidget.clear()
        self.tableWidget.setColumnCount(3)
        for i in range(3):
            self.tableWidget.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())
        self.tableRename()

        self.component_enable_ui = {}
        self.tableWidget.setRowCount(len(component_dict))
        row = 0

        for component_identifier in component_dict:
            self.tableWidget.setRowHeight(row,70)
            component_info = component_dict[component_identifier]
            new_item = QtWidgets.QTableWidgetItem(component_info["name"])
            new_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(row, 0, new_item)
            description = QtWidgets.QTextBrowser()
            description.setObjectName("description")
            self.tableWidget.setCellWidget(row,1,description)
            enable = QtWidgets.QCheckBox()
            enable.setObjectName("enable")
            hLayout = QtWidgets.QHBoxLayout()
            hLayout.addWidget(enable)
            hLayout.setAlignment(enable, Qt.AlignCenter)
            widget = QtWidgets.QWidget()
            widget.setLayout(hLayout)
            self.tableWidget.setCellWidget(row, 2, widget)

            description.setText(component_info["description"])
            enable.setChecked(component_info["is_checked"])

            self.component_enable_ui[component_identifier] = enable

            row += 1

    def tableRename(self):
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText("name")
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText("description")
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText("enable")

    def rename(self):
        self.dialog.setWindowTitle("components")
        self.search.setPlaceholderText("search")
        self.tableRename()

    def bind(self):
        self.DialogButtonBox.rejected.connect(self.dialog.close)
        # self.DialogButtonBox.accepted.connect(self.ok) # 这样写点击按钮没反应
        self.DialogButtonBox.accepted.connect(lambda:self.ok()) # 但是这样写可以
        self.search.textChanged.connect(self.searchTextChanged)

    def ok(self):
        component_enable = {}
        for identifier in self.component_dict:
            component_enable[identifier] = self.component_enable_ui[identifier].isChecked()
        self.callback_func(component_enable)
        self.dialog.close()

    def init(self):
        self.tableWidget.setColumnWidth(0, 100)
        self.tableWidget.setColumnWidth(1, 440)
        self.tableWidget.setColumnWidth(2, 10)
        self.tableWidget.verticalHeader().hide()
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.rename()
        self.bind()

    def setupUi(self,ui_system,Dialog):
        super(AskComponent, self).setupUi(Dialog)
        self.dialog = Dialog
        self.ui_system = ui_system

    def searchTextChanged(self, keyword):
        if keyword == "":
            self.showComponents(self.component_dict)
            return
        matching_components_dict = {}
        for identifier in self.component_dict:
            if keyword in identifier:
                matching_components_dict[identifier] = self.component_dict[identifier]
        self.showComponents(matching_components_dict)


class Setting(setting.Ui_Dialog,UiBasic):
    def setupUi(self, ui_system,Dialog):
        self.dialog = Dialog
        self.ui_system = ui_system
        super(Setting, self).setupUi(Dialog)

    def rename(self):
        self.dialog.setWindowTitle("setting")
        self.Individuation.setTitle("Individuation")
        self.theme_text.setText("theme")
        self.language_text.setText("language")
        self.Update.setTitle("Update")
        self.c_v_text.setText("Current version")
        self.c_v.setText("")
        self.l_v_text.setText("Latest version")
        self.l_v.setText("")
        self.check_n_v.setText("Check the new version")
        self.Other.setTitle("Other")
        self.clear_cache.setText("ClearCache")

    def bind(self):
        self.clear_cache.clicked.connect(lambda:lib.clearFolder("tmp"))

    def init(self):
        self.language.clear()
        self.languages = {}
        languages = []
        for folder in os.listdir("lang"):
            languages_info = {}
            self.languages[folder] = {}
            with open(f"./lang/{folder}/language","r",encoding="utf-8") as f:
                for line in f.readlines():
                    line = line[:-1]
                    if "=" not in line:
                        continue
                    key,value = line.split("=")
                    languages_info[key] = value
                    self.languages[folder][key] = value
            languages.append(languages_info["name"])
        self.language.addItems(languages)

        self.language.setCurrentText(self.languages[self.ui_system.MainSystem.config["lang"]]["name"])
        self.rename()
        self.bind()

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

    def showDialog(self,ui_obj):
        dialog = QDialog(self)
        ui_obj.setupUi(self,dialog)
        ui_obj.init()
        dialog.show()
