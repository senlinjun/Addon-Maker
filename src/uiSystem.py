import random, lib, addon
from os import listdir
from ui import start,addonUi,addon_setting,ask_components,setting
from PyQt5 import QtGui, QtWidgets
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
        self.uiSystem.setWindowTitle(self.uiSystem.MainSystem.lang["ui","start_title"])
        self.new_addon.setText(
            f'{self.uiSystem.MainSystem.lang["ui","new"]} {self.uiSystem.MainSystem.lang["ui","bedrock_addon"]}'
        )
        self.new_mod.setText(
            f'{self.uiSystem.MainSystem.lang["ui","new"]} {self.uiSystem.MainSystem.lang["ui","java_mod"]}'
        )
        self.open.setText(self.uiSystem.MainSystem.lang["ui","open"])
        self.setting.setText(self.uiSystem.MainSystem.lang["ui","setting_title"])
        self.notice_box.setTitle(self.uiSystem.MainSystem.lang["ui","notice"])

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
        self.updateContentList()

    def rename(self):
            self.uiSystem.setWindowTitle(f'{self.uiSystem.MainSystem.lang["ui","addon"]}({self.uiSystem.MainSystem.project_object.packname})')
            self.content_tab.setTabText(0, self.uiSystem.MainSystem.lang["ui", "content_all"])
            self.content_tab.setTabText(1, self.uiSystem.MainSystem.lang["ui", "content_block"])
            self.content_tab.setTabText(2, self.uiSystem.MainSystem.lang["ui", "content_item"])
            self.content_tab.setTabText(3, self.uiSystem.MainSystem.lang["ui", "content_entity"])
            self.content_tab.setTabText(4, self.uiSystem.MainSystem.lang["ui", "content_feature"])
            self.content_tab.setTabText(5, self.uiSystem.MainSystem.lang["ui", "content_recipe"])
            self.addItem.setText("+")
            self.removeItem.setText("-")
            self.data_tab.setTabText(0,self.uiSystem.MainSystem.lang["ui","behavior"])
            self.data_tab.setTabText(1,self.uiSystem.MainSystem.lang["ui","resource"])
            self.modifyComponents.setText("...")
            self.menuFile.setTitle(self.uiSystem.MainSystem.lang["ui","file"])
            self.menuNew.setTitle(self.uiSystem.MainSystem.lang["ui","new"])
            self.actionBedrock_Addon.setText(self.uiSystem.MainSystem.lang["ui","bedrock_addon"])
            self.actionJava_Mod.setText(self.uiSystem.MainSystem.lang["ui","java_mod"])
            self.actionOpen.setText(self.uiSystem.MainSystem.lang["ui","open"])
            self.actionSave.setText(self.uiSystem.MainSystem.lang["ui","save"])
            self.actionExport.setText(self.uiSystem.MainSystem.lang["ui","export"])

    def updateContentList(self):
        self.all_list.clear()
        self.block_list.clear()
        self.item_list.clear()
        self.entity_list.clear()
        self.feature_list.clear()
        self.recipe_list.clear()

        # blocks
        blocks_identifier = [key for key in self.uiSystem.MainSystem.project_object.blocks]
        blocks_identifier.sort()
        self.all_list.addItems([f'[{self.uiSystem.MainSystem.lang["ui","content_block"]}] {identifier}' for identifier in blocks_identifier])
        self.block_list.addItems([f'[{self.uiSystem.MainSystem.lang["ui","content_block"]}] {identifier}' for identifier in blocks_identifier])

    def bind(self):
        self.addItem.clicked.connect(self.addContent)
        self.removeItem.clicked.connect(self.removeContent)
        self.actionSave.triggered.connect(self.save)
        self.actionOpen.triggered.connect(self.uiSystem.MainSystem.askOpenProject)
        self.actionBedrock_Addon.triggered.connect(lambda:self.uiSystem.changeUi(AddonSetting(self)))
        self.actionExport.triggered.connect(self.export)
        for l in [self.all_list,self.block_list,self.item_list,self.entity_list,self.feature_list,self.recipe_list]:
            l.itemClicked.connect(self.updateComponent)
        self.modifyComponents.clicked.connect(self.clickedModifyComponent)

    def addContent(self):
        current_text = self.content_tab.tabText(self.content_tab.currentIndex())
        if current_text == self.uiSystem.MainSystem.lang["ui","content_all"]:
            select = QInputDialog.getItem(
                self.uiSystem,
                self.uiSystem.MainSystem.lang["ui","add_content"],
                self.uiSystem.MainSystem.lang["ui","add_content_label"],
                [
                    self.uiSystem.MainSystem.lang["ui","content_block"],
                    self.uiSystem.MainSystem.lang["ui","content_block"],
                    self.uiSystem.MainSystem.lang["ui","content_entity"],
                    self.uiSystem.MainSystem.lang["ui","content_feature"],
                    self.uiSystem.MainSystem.lang["ui","content_recipe"]
                ],
                current=0,
                editable=False
            )
            if not select[1]:
                return
            item = select[0]
            if item == self.uiSystem.MainSystem.lang["ui","content_block"]:
                self.addContentBlock()
        elif current_text == self.uiSystem.MainSystem.lang["ui","content_block"]:
            self.addContentBlock()

    def addContentBlock(self):
        new_block_input = QInputDialog.getText(
            self.uiSystem,
            self.uiSystem.MainSystem.lang["ui","new_block"],
            self.uiSystem.MainSystem.lang["ui","new_block_label"],
            text=f"{self.uiSystem.MainSystem.project_object.namespace}:"
        )
        if not new_block_input[1]:
            return
        identifier = new_block_input[0]
        if identifier.find(" ") != -1:
            QMessageBox.critical(self.uiSystem, self.uiSystem.MainSystem.lang["ui","error"], self.uiSystem.MainSystem.lang["ui","cannot_contain_spaces"])
            return
        if identifier == "":
            QMessageBox.critical(self.uiSystem, self.uiSystem.MainSystem.lang["ui","error"], self.uiSystem.MainSystem.lang["ui","cannot_leave_blank"])
            return
        namespace,id = identifier.split(":")

        new_block = addon.Block(self.uiSystem.MainSystem.project_object)
        new_block.new(namespace,id)
        self.uiSystem.MainSystem.project_object.blocks[new_block.identifier] = new_block
        self.updateContentList()

    def removeContent(self):
        return_back = self.getSelectContent()
        if return_back == None:
            return
        content_type, content = return_back
        content.remove()
        self.updateContentList()

    def getSelectContent(self):
        """
        :return:
        (type,content)/None
        """
        tab_index = self.content_tab.currentIndex()
        contents_dict = {0:self.all_list,1:self.block_list,2:self.item_list,3:self.entity_list,4:self.feature_list,5:self.recipe_list}
        content = contents_dict[tab_index].currentItem()
        if content is None:
            return None
        content_text = content.text()
        content_type,content_identifier = content_text.split(" ")
        if content_type == f'[{self.uiSystem.MainSystem.lang["ui","content_block"]}]':
            return content_type, self.uiSystem.MainSystem.project_object.blocks[content_identifier]

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

    def updateComponent(self):
        self.clearLayout(self.behavior_layout)
        self.clearLayout(self.resource_layout)
        content = self.getSelectContent()
        if content is None:
            return
        self.component_ui = {}
        content_type,content = content
        for component_identifier in content.components:
            component_data_obj = content.components[component_identifier]
            ui_dict = component_data_obj.getUiDict()
            group_box = QtWidgets.QGroupBox(self.behavior_scrollAreaWidgetContents)
            group_box.setObjectName("groupBox")
            form_layout = QtWidgets.QFormLayout(group_box)
            form_layout.setObjectName("formLayout")
            self.component_ui[component_identifier] = self.setComponentUi(group_box, form_layout, ui_dict, component_data_obj.identifier)
            self.behavior_layout.addWidget(group_box)

    def setComponentUi(self, group_box, form_layout, data_dict:dict, component_identifier:str):
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
                child = self.setComponentUi(new_group_box, new_form_layout, data_dict[key], component_identifier)
                field = new_group_box

            value, value_type, value_limit = data_dict[key]

            if value_type == "bool":
                field = QtWidgets.QCheckBox(group_box)
                field.setObjectName("checkBox")
                field.setChecked(value)
                field.stateChanged.connect(lambda:self.componentChanged(field))

            elif value_type == "int":
                field = QtWidgets.QSpinBox(group_box)
                field.setObjectName("spinBox")
                if value_limit is not None:
                    field.setMinimum(value_limit[0])
                    field.setMaximum(value_limit[1])
                field.setValue(value)
                field.valueChanged.connect(lambda:self.componentChanged(field))

            elif value_type == "float":
                field = QtWidgets.QDoubleSpinBox(group_box)
                field.setObjectName("doubleSpinBox")
                if value_limit is not None:
                    field.setMinimum(value_limit[0])
                    field.setMaximum(value_limit[1])
                field.setValue(value)
                field.valueChanged.connect(lambda:self.componentChanged(field))

            elif value_type == "str":
                field = QtWidgets.QLineEdit(group_box)
                field.setObjectName("lineEdit")
                if value_limit is not None:
                    field.setMaxLength(value_limit)
                field.setText(value)
                field.textChanged.connect(lambda:self.componentChanged(field))

            if field is None:
                field = QtWidgets.QLabel(group_box)
                field.setObjectName("label")
                field.setText(self.uiSystem.MainSystem.lang["ui","unsupported_type"])

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

    def componentChanged(self, item):
        ui_dict = self.component_ui[item.identifier]
        content_adj = self.getSelectContent()
        if content_adj is None:
            return
        component_data_obj = content_adj[1].components[item.identifier]
        component_data_obj.parseFromUi(ui_dict)
        self.updateComponent()

    def clickedModifyComponent(self):
        content = self.getSelectContent()
        if content is None:
            return
        content_type,content = content

        dialog = AskComponent(content.getBehaviorComponents(),self.modifyComponentCallback)
        self.uiSystem.showDialog(dialog)
        dialog.showComponents()

    def modifyComponentCallback(self,component_dict):
        content = self.getSelectContent()
        if content is None:
            return
        content_type, content = content
        for component_data in component_dict:
            if component_data in content.components and not component_dict[component_data]:
                content.components.pop(component_data)
            elif component_data not in content.components and component_dict[component_data]:
                content.addBehaviorComponent(component_data)
        self.updateComponent()


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
        self.uiSystem.setWindowTitle(self.uiSystem.MainSystem.lang["ui","addon_setting_title"])
        self.description_label_2.setText(self.uiSystem.MainSystem.lang["ui","description"])
        self.namespace_label.setText(self.uiSystem.MainSystem.lang["ui","namespace"])
        self.random_namepace.setText(self.uiSystem.MainSystem.lang["ui","random"])
        self.packName_label.setText(self.uiSystem.MainSystem.lang["ui","packname"])
        self.pack_version_label.setText(self.uiSystem.MainSystem.lang["ui","pack_version"])
        self.label_4.setText(".")
        self.label_3.setText(".")
        self.game_version_label.setText(self.uiSystem.MainSystem.lang["ui","game_minimum_version"])
        self.icon_label.setText(self.uiSystem.MainSystem.lang["ui","pack_icon"])
        self.choose_icon.setText(self.uiSystem.MainSystem.lang["ui","choose"])
        self.Ok.setText(self.uiSystem.MainSystem.lang["ui","ok"])
        self.Cancel.setText(self.uiSystem.MainSystem.lang["ui","cancel"])

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
            blank.append(self.uiSystem.MainSystem.lang["ui","packname"])
        if self.namespace_2.text() == "":
            blank.append(self.uiSystem.MainSystem.lang["ui","namespace"])
        if not blank:
            return True

        message = f"{self.uiSystem.MainSystem.lang['ui','cannot_leave_blank']}\n("
        for name in blank:
            message += name
            message += ','
        message = message[:-1]+')'
        QMessageBox.critical(self.uiSystem, self.uiSystem.MainSystem.lang["ui","error"], message)
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
            enable.component_identifier = component_identifier
            enable.stateChanged.connect(lambda:self.enableStateChanged(enable))
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
        item.setText(self.ui_system.MainSystem.lang["ui","name"])
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(self.ui_system.MainSystem.lang["ui","description"])
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(self.ui_system.MainSystem.lang["ui","enable"])

    def rename(self):
        self.dialog.setWindowTitle(self.ui_system.MainSystem.lang["ui","ask_component_title"])
        self.search.setPlaceholderText(self.ui_system.MainSystem.lang["ui","search"])
        self.ok_button.setText(self.ui_system.MainSystem.lang["ui","ok"])
        self.cancel_button.setText(self.ui_system.MainSystem.lang["ui","cancel"])
        self.tableRename()

    def bind(self):
        self.cancel_button.clicked.connect(self.dialog.close)
        # self.DialogButtonBox.accepted.connect(self.ok) # 这样写点击按钮没反应
        self.ok_button.clicked.connect(lambda:self.ok()) # 但是这样写可以
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
            component_info = self.component_dict[identifier]
            if keyword in component_info["name"]:
                matching_components_dict[identifier] = self.component_dict[identifier]
        self.showComponents(matching_components_dict)

    def enableStateChanged(self,enable):
        self.component_dict[enable.component_identifier]["is_checked"] = enable.isChecked()

class Setting(setting.Ui_Dialog,UiBasic):
    def setupUi(self, ui_system,Dialog):
        self.dialog = Dialog
        self.ui_system = ui_system
        super(Setting, self).setupUi(Dialog)

    def rename(self):
        self.dialog.setWindowTitle(self.ui_system.MainSystem.lang["ui","setting_title"])
        self.Individuation.setTitle(self.ui_system.MainSystem.lang["ui","individuation"])
        self.theme_text.setText(self.ui_system.MainSystem.lang["ui","theme"])
        self.language_text.setText(self.ui_system.MainSystem.lang["ui","language"])
        self.Update.setTitle(self.ui_system.MainSystem.lang["ui","update"])
        self.c_v_text.setText(self.ui_system.MainSystem.lang["ui","current_version"])
        self.c_v.setText("")
        self.l_v_text.setText(self.ui_system.MainSystem.lang["ui","latest_version"])
        self.l_v.setText("")
        self.check_n_v.setText(self.ui_system.MainSystem.lang["ui","check_new_version"])
        self.Other.setTitle(self.ui_system.MainSystem.lang["ui","other"])
        self.clear_cache.setText(self.ui_system.MainSystem.lang["ui","clear_cache"])

    def bind(self):
        self.clear_cache.clicked.connect(lambda:lib.clearFolder("tmp"))
        self.language.currentTextChanged.connect(lambda:self.languageChanged())
        self.theme.currentTextChanged.connect(lambda:self.themeChanged())

    def init(self):
        self.language.clear()
        self.theme.clear()
        self.languages = {}
        for folder in listdir("lang"):
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
            self.language.addItem(languages_info["name"])

        for file in listdir("theme"):
            theme_name = file.replace(".qss","")
            self.theme.addItem(theme_name)
        self.theme.setCurrentText(self.ui_system.MainSystem.config["theme"])

        self.language.setCurrentText(self.languages[self.ui_system.MainSystem.config["lang"]]["name"])
        self.rename()
        self.bind()

    def languageChanged(self):
        language = self.language.currentText()
        for lang_id in self.languages:
            if self.languages[lang_id]["name"] == language:
                self.ui_system.MainSystem.loadLanguage(lang_id)
                self.ui_system.ui.rename()
                self.ui_system.dialog_ui.rename()
                self.ui_system.MainSystem.config["lang"] = lang_id
                return

    def themeChanged(self):
        theme = self.theme.currentText()
        self.ui_system.loadTheme(theme)

class UiSystem(QMainWindow):
    def __init__(self,MainSystem,Ui=StartUi()):
        super().__init__()
        self.MainSystem = MainSystem
        self.ui = None
        self.dialog = None
        self.dialog_ui = None
        self.style_sheet = None
        self.loadTheme(self.MainSystem.config["theme"])
        self.changeUi(Ui)

    def loadTheme(self,theme):
        self.MainSystem.config["theme"] = theme
        if f'{self.MainSystem.config["theme"]}.qss' not in listdir('theme'):
            self.MainSystem.config["theme"] = "Default"
        with open(f"./theme/{self.MainSystem.config['theme']}.qss") as f:
            self.style_sheet = f.read()
        self.setStyleSheet(self.style_sheet)

    def changeUi(self,ui_obj):
        self.ui = ui_obj
        self.ui.setupUi(self)
        self.ui.init()

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.ui.close_callback:
            event.ignore()
            self.ui.close()

    def showDialog(self,ui_obj):
        self.dialog_ui = ui_obj
        if self.dialog:
            self.dialog.close()
        self.dialog = QDialog(self)
        self.dialog_ui.setupUi(self,self.dialog)
        self.dialog_ui.init()
        self.dialog.show()
