import os
import random, lib, sys, addon, os, json

from ui import start,addonUi,addon_setting
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow, QFileDialog,QMessageBox,QInputDialog
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
        projects = self.getRecentList()
        self.recent_list.addItems(projects)

    def rename(self):
        _translate = QtCore.QCoreApplication.translate
        self.uiSystem.setWindowTitle(_translate("Form", "Start"))
        self.new_addon.setText(_translate("Form", "New Bedrock Addon"))
        self.new_mod.setText(_translate("Form", "New Java Mod"))
        self.open.setText(_translate("Form", "Open"))
        self.setting.setText(_translate("Form", "setting"))
        self.recent.setTitle(_translate("Form", "recent"))

    def bind(self):
        self.new_addon.clicked.connect(lambda:self.uiSystem.changeUi(AddonSetting(self)))
        self.recent_list.itemClicked.connect(self.clickedRecentProject)
        self.open.clicked.connect(self.uiSystem.MainSystem.askOpenProject)

    def clickedRecentProject(self,project):
        self.uiSystem.MainSystem.openProject(f"./works/{project.text()}")

    def getRecentList(self):
        projects = os.listdir("./works/")
        projects.sort(key=self.recentSortTakeKey,reverse=True)
        return projects

    def recentSortTakeKey(self,project):
        with open(f"./works/{project}/project.json","r") as f:
            project_data = json.load(f)
        return project_data["modification_time"]

class AddonUi(addonUi.Ui_MainWindow, UiBasic):
    def setupUi(self, uiSystem):
        super().setupUi(uiSystem)
        self.uiSystem = uiSystem

    def init(self):
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
        for component_list in [self.all_list,self.block_list,self.item_list,self.entity_list,self.feature_list,self.recipe_list]:
            component_list.itemClicked.connect(self.updateComponentData)

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
        new_block_input = QInputDialog.getText(self.uiSystem,"newBlock","Enter the id of the New Block")
        if not new_block_input[1]:
            return
        id = new_block_input[0]
        if id.find(" ") != -1:
            QMessageBox.critical(self.uiSystem, "error", "Cannot contain Spaces")
            return

        new_block = addon.Block(self.uiSystem.MainSystem.project_object)
        new_block.new(id)
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
        '''
        :return:
        (type,component)
        '''
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
        self.uiSystem.MainSystem.project_object.save()

    def updateComponentData(self):
        self.clearLayout(self.behavior_data_layout)
        self.clearLayout(self.resource_data_layout)
        component = self.getSelectComponent()
        if component is None:
            return
        component_type,component = component
        behavior_data = component.getBehaviorData()
        for key in behavior_data:
            self.addFormLine(key,behavior_data[key],self.behavior_data_layout,self.behavior)

        resource_data = component.getResourceData()
        for key in resource_data:
            self.addFormLine(key, resource_data[key], self.resource_data_layout, self.resource)

    def setFormLine(self,key,value,layout,tab,line):
        label = QtWidgets.QLabel(tab)
        label.setObjectName("label")
        label.setText(key)
        layout.setWidget(line, QtWidgets.QFormLayout.LabelRole, label)
        field = None
        if isinstance(value,str):
            field = QtWidgets.QLineEdit(tab)
            field.setText(value)
        elif isinstance(value,bool):
            field = QtWidgets.QCheckBox(tab)
            field.setChecked(value)
        elif isinstance(value,int):
            field = QtWidgets.QSpinBox(tab)
            field.setValue(value)
        elif isinstance(value,float):
            field = QtWidgets.QDoubleSpinBox(tab)
            field.setValue(value)
        if field is None:
            return
        layout.setWidget(line, QtWidgets.QFormLayout.FieldRole, field)

    def clearLayout(self,layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)
            item.widget().deleteLater()

    def addFormLine(self,key,value,layout,tab):
        self.setFormLine(key,value,layout,tab,layout.rowCount())

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
            self.uiSystem.MainSystem.project_object = addon.BedrockAddon()
            self.uiSystem.MainSystem.project_object.new(
                "./works",
                2,
                self.packName.text(),
                self.description.toPlainText(),
                self.namespace_2.text(),
                [int(self.pack_version_0.text()),int(self.pack_version_1.text()),int(self.pack_version_2.text())],
                [int(number) for number in self.choose_detailed_version.currentText().split(".")]
            )
            self.uiSystem.MainSystem.project_object.save()
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