import addon
import lib
from random import randint
from os import listdir
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication, Qt
from PyQt5.QtWidgets import (
    QMainWindow,
    QFileDialog,
    QMessageBox,
    QInputDialog,
    QDialog,
    QAbstractItemView,
    QHeaderView,
)
from data.addon import BlockBehavior, BlockResource, BlockTrigger, BlockEventResponses

from ui import (
    start,
    addonUi,
    addon_setting,
    ask_components,
    setting,
    ask_list,
    ask_events,
)


class UiBasic:
    def __init__(self):
        self.close_callback = False
        self.drop_callback = False

    def close(self):
        pass

    def init(self):
        pass

    def drop(self, text):
        pass


class StartUi(start.Ui_MainWindow, UiBasic):
    def setupUi(self, uiSystem):
        super().setupUi(uiSystem)
        self.uiSystem = uiSystem

    def init(self):
        self.rename()
        self.bind()
        img = QtGui.QPixmap("./resources/start.png")
        self.img.setPixmap(img)
        self.drop_callback = True

    def rename(self):
        self.uiSystem.setWindowTitle(self.uiSystem.MainSystem.lang["ui", "start_title"])
        self.new_addon.setText(
            f'{self.uiSystem.MainSystem.lang["ui","new"]} {self.uiSystem.MainSystem.lang["ui","bedrock_addon"]}'
        )
        self.new_mod.setText(
            f'{self.uiSystem.MainSystem.lang["ui","new"]} {self.uiSystem.MainSystem.lang["ui","java_mod"]}'
        )
        self.open.setText(self.uiSystem.MainSystem.lang["ui", "open"])
        self.setting.setText(self.uiSystem.MainSystem.lang["ui", "setting_title"])
        self.notice_box.setTitle(self.uiSystem.MainSystem.lang["ui", "notice"])

    def bind(self):
        self.new_addon.clicked.connect(self.addonClicked)
        self.open.clicked.connect(self.uiSystem.MainSystem.askOpenProject)
        self.setting.clicked.connect(lambda: self.uiSystem.showDialog(Setting()))

    def addonClicked(self):
        self.uiSystem.changeUi(AddonSetting(self))

    def drop(self, file: str):
        file_path = file.replace("file:///", "")
        self.uiSystem.MainSystem.openProject(file_path)


class AddonUi(addonUi.Ui_MainWindow, UiBasic):
    def setupUi(self, uiSystem):
        super().setupUi(uiSystem)
        self.uiSystem = uiSystem

    def init(self):
        self.component_ui = {}
        self.close_callback = True
        self.drop_callback = True
        self.rename()
        self.bind()
        self.updateContentList()
        self.showImportItems()
        self.modifyComponents.setEnabled(False)

    def rename(self):
        self.uiSystem.setWindowTitle(
            f'{self.uiSystem.MainSystem.lang["ui","addon"]}({self.uiSystem.MainSystem.project_object.packname})'
        )
        self.content_tab.setTabText(
            0, self.uiSystem.MainSystem.lang["ui", "content_all"]
        )
        self.content_tab.setTabText(
            1, self.uiSystem.MainSystem.lang["ui", "content_block"]
        )
        self.content_tab.setTabText(
            2, self.uiSystem.MainSystem.lang["ui", "content_item"]
        )
        self.content_tab.setTabText(
            3, self.uiSystem.MainSystem.lang["ui", "content_entity"]
        )
        self.content_tab.setTabText(
            4, self.uiSystem.MainSystem.lang["ui", "content_feature"]
        )
        self.content_tab.setTabText(
            5, self.uiSystem.MainSystem.lang["ui", "content_recipe"]
        )
        self.addItem.setText("+")
        self.removeItem.setText("-")
        self.component_tab.setTabText(
            0, self.uiSystem.MainSystem.lang["ui", "behavior"]
        )
        self.component_tab.setTabText(
            1, self.uiSystem.MainSystem.lang["ui", "resource"]
        )
        self.menuFile.setTitle(self.uiSystem.MainSystem.lang["ui", "file"])
        self.menuNew.setTitle(self.uiSystem.MainSystem.lang["ui", "new"])
        self.actionBedrock_Addon.setText(
            self.uiSystem.MainSystem.lang["ui", "bedrock_addon"]
        )
        self.actionJava_Mod.setText(self.uiSystem.MainSystem.lang["ui", "java_mod"])
        self.actionOpen.setText(self.uiSystem.MainSystem.lang["ui", "open"])
        self.actionSave.setText(self.uiSystem.MainSystem.lang["ui", "save"])
        self.actionExport.setText(self.uiSystem.MainSystem.lang["ui", "export"])
        self.imported_items_tab.setTabText(
            0, self.uiSystem.MainSystem.lang["ui", "textures"]
        )
        self.modifyComponents.setText("...")
        self.data_tab.setTabText(0,self.uiSystem.MainSystem.lang["ui","components"])
        self.data_tab.setTabText(1, self.uiSystem.MainSystem.lang["ui", "events"])
        self.event_tab.setTabText(0, self.uiSystem.MainSystem.lang["ui", "trigger"])
        self.event_tab.setTabText(1, self.uiSystem.MainSystem.lang["ui", "event_response"])
        self.showComponent()

    def updateContentList(self):
        self.all_list.clear()
        self.block_list.clear()
        self.item_list.clear()
        self.entity_list.clear()
        self.feature_list.clear()
        self.recipe_list.clear()

        # blocks
        blocks_identifier = [
            key for key in self.uiSystem.MainSystem.project_object.blocks
        ]
        blocks_identifier.sort()
        self.all_list.addItems(
            [
                f'[{self.uiSystem.MainSystem.lang["ui","content_block"]}] {identifier}'
                for identifier in blocks_identifier
            ]
        )
        self.block_list.addItems(
            [
                f'[{self.uiSystem.MainSystem.lang["ui","content_block"]}] {identifier}'
                for identifier in blocks_identifier
            ]
        )

    def bind(self):
        self.addItem.clicked.connect(self.addContent)
        self.removeItem.clicked.connect(self.removeContent)
        self.actionSave.triggered.connect(self.save)
        self.actionOpen.triggered.connect(self.uiSystem.MainSystem.askOpenProject)
        self.actionBedrock_Addon.triggered.connect(
            lambda: self.uiSystem.changeUi(AddonSetting(self))
        )
        self.actionExport.triggered.connect(self.export)
        for l in [
            self.all_list,
            self.block_list,
            self.item_list,
            self.entity_list,
            self.feature_list,
            self.recipe_list,
        ]:
            l.itemClicked.connect(self.showComponent)
        self.modifyComponents.clicked.connect(self.clickedModifyComponent)
        self.event_tab.currentChanged.connect(self.eventTabChanged)

        self.import_button.clicked.connect(self.importTexture)
        self.delete_button.clicked.connect(self.deleteImportItem)

    def addContent(self):
        current_text = self.content_tab.tabText(self.content_tab.currentIndex())
        if current_text == self.uiSystem.MainSystem.lang["ui", "content_all"]:
            select = QInputDialog.getItem(
                self.uiSystem,
                self.uiSystem.MainSystem.lang["ui", "add_content"],
                self.uiSystem.MainSystem.lang["ui", "add_content_label"],
                [
                    self.uiSystem.MainSystem.lang["ui", "content_block"],
                    self.uiSystem.MainSystem.lang["ui", "content_block"],
                    self.uiSystem.MainSystem.lang["ui", "content_entity"],
                    self.uiSystem.MainSystem.lang["ui", "content_feature"],
                    self.uiSystem.MainSystem.lang["ui", "content_recipe"],
                ],
                current=0,
                editable=False,
            )
            if not select[1]:
                return
            item = select[0]
            if item == self.uiSystem.MainSystem.lang["ui", "content_block"]:
                self.addContentBlock()
        elif current_text == self.uiSystem.MainSystem.lang["ui", "content_block"]:
            self.addContentBlock()

    def addContentBlock(self):
        new_block_input = QInputDialog.getText(
            self.uiSystem,
            self.uiSystem.MainSystem.lang["ui", "new_block"],
            self.uiSystem.MainSystem.lang["ui", "new_block_label"],
            text=f"{self.uiSystem.MainSystem.project_object.namespace}:",
        )
        if not new_block_input[1]:
            return
        identifier = new_block_input[0]
        if identifier.find(" ") != -1:
            QMessageBox.critical(
                self.uiSystem,
                self.uiSystem.MainSystem.lang["ui", "error"],
                self.uiSystem.MainSystem.lang["ui", "cannot_contain_spaces"],
            )
            return
        if identifier == "":
            QMessageBox.critical(
                self.uiSystem,
                self.uiSystem.MainSystem.lang["ui", "error"],
                self.uiSystem.MainSystem.lang["ui", "cannot_leave_blank"],
            )
            return
        namespace, id = identifier.split(":")

        new_block = addon.Block(self.uiSystem.MainSystem.project_object)
        new_block.new(namespace, id)
        self.uiSystem.MainSystem.project_object.blocks[new_block.identifier] = new_block
        self.updateContentList()

    def removeContent(self):
        return_back = self.getSelectContent()
        if return_back == None:
            return
        content_type, content = return_back
        content.remove()
        self.updateContentList()
        self.showComponent()

    def getSelectContent(self):
        """
        :return:
        (type,content)/None
        """
        tab_index = self.content_tab.currentIndex()
        contents_dict = {
            0: self.all_list,
            1: self.block_list,
            2: self.item_list,
            3: self.entity_list,
            4: self.feature_list,
            5: self.recipe_list,
        }
        content = contents_dict[tab_index].currentItem()
        if content is None:
            return None
        content_text = content.text()
        content_type, content_identifier = content_text.split(" ")
        if content_type == f'[{self.uiSystem.MainSystem.lang["ui","content_block"]}]':
            return (
                content_type,
                self.uiSystem.MainSystem.project_object.blocks[content_identifier],
            )

    def save(self):
        if self.uiSystem.MainSystem.project_object.save_path is None:
            save_path = QFileDialog.getSaveFileName(
                self.uiSystem, filter="'amproject(*.amproject)'"
            )[0]
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

    def showComponent(self):
        lib.clearLayout(self.behavior_layout)
        lib.clearLayout(self.resource_layout)
        lib.clearLayout(self.trigger_layout)
        content = self.getSelectContent()
        if content is None:
            self.modifyComponents.setEnabled(False)
            return
        self.modifyComponents.setEnabled(True)
        content_type, content = content
        self.component_ui = {}
        components = {
            "behavior": (
                content.behavior_components,
                self.behavior_scrollAreaWidgetContents,
                self.behavior_layout,
            ),
            "resource": (
                content.resource_components,
                self.resource_scrollAreaWidgetContents,
                self.resource_layout,
            ),
            "trigger": (
                content.triggers,
                self.trigger_scrollAreaWidgetContents,
                self.trigger_layout,
            ),
        }
        for key in components:
            size = 20
            for component_identifier in components[key][0]:
                component_data_obj = components[key][0][component_identifier]
                ui_dict = component_data_obj.getUiDict()
                group_box = QtWidgets.QGroupBox(components[key][1])
                group_box.setObjectName("groupBox")
                group_box.setTitle(
                    self.uiSystem.MainSystem.lang[
                        "addon", f"{component_identifier}_name"
                    ]
                )
                form_layout = QtWidgets.QFormLayout(group_box)
                form_layout.setObjectName("formLayout")
                (
                    self.component_ui[component_identifier],
                    component_ui_size,
                ) = self.uiSystem.MainSystem.setDataUi(
                    group_box,
                    form_layout,
                    ui_dict,
                    component_data_obj.identifier,
                    key,
                    self.componentChanged,
                )
                size += component_ui_size
                components[key][2].addWidget(group_box)
            components[key][1].setGeometry(0, 0, 630, size)

    def componentChanged(self, component_type, **args):
        if component_type == "list":
            list_name = args["list_name"]
            list_ = args["list_"]
            self.component_ui["properties"][list_name].component_list = list_
            self.componentChanged(self.component_ui["properties"][list_name])
            return

        item = args["item"]
        ui_dict = self.component_ui[item.identifier]
        content_adj = self.getSelectContent()
        if content_adj is None:
            return
        component_data_obj = None
        if item.type == "behavior":
            component_data_obj = content_adj[1].behavior_components[item.identifier]
        elif item.type == "resource":
            component_data_obj = content_adj[1].resource_components[item.identifier]
        elif item.type == "trigger":
            component_data_obj = content_adj[1].triggers[item.identifier]
        if component_data_obj is not None:
            component_data_obj.parseFromUi(ui_dict)
            self.showComponent()

    def clickedModifyComponent(self):
        content = self.getSelectContent()
        if content is None:
            return
        content_type, content = content
        data_tab_index = self.data_tab.currentIndex()
        tab_index = self.component_tab.currentIndex()
        component_dict = {}
        if data_tab_index == 1:
            component_dict = content.getTriggers()
        elif tab_index == 0:
            component_dict = content.getBehaviorComponents()
        elif tab_index == 1:
            component_dict = content.getResourceComponents()
        dialog = AskComponent(component_dict, self.modifyComponentCallback)
        self.uiSystem.showDialog(dialog)
        dialog.showComponents()

    def modifyComponentCallback(self, component_dict):
        content = self.getSelectContent()
        if content is None:
            return
        content_type, content = content
        data_tab_index = self.data_tab.currentIndex()
        tab_index = self.component_tab.currentIndex()
        components = {}
        if data_tab_index == 1:
            components = content.triggers
        elif tab_index == 0:
            components = content.behavior_components
        elif tab_index == 1:
            components = content.resource_components
        for component_identifier in component_dict:
            if (
                component_identifier in components
                and not component_dict[component_identifier]
            ):
                components.pop(component_identifier)
            elif (
                component_identifier not in components
                and component_dict[component_identifier]
            ):
                if data_tab_index == 1:
                    components[component_identifier] = BlockTrigger.triggers[
                        component_identifier
                    ](content, self.uiSystem)
                elif tab_index == 0:
                    components[component_identifier] = BlockBehavior.components[
                        component_identifier
                    ](content, self.uiSystem)
                elif tab_index == 1:
                    components[component_identifier] = BlockResource.components[
                        component_identifier
                    ](content, self.uiSystem)
        if data_tab_index == 1:
            content.triggers = components
        elif tab_index == 0:
            content.behavior_components = components
        elif tab_index == 1:
            content.resource_components = components
        self.showComponent()

    def drop(self, file):
        file_path = file.replace("file:///", "")
        self.uiSystem.MainSystem.openProject(file_path)

    def importTexture(self):
        file_path = QFileDialog.getOpenFileName(
            self.uiSystem,
            self.uiSystem.MainSystem.lang["ui", "open"],
            filter="'png(*.png)'",
        )[0]
        if file_path == "":
            return
        file_name = "".join(file_path.split("/")[-1].split(".")[:-1])
        input_ = QInputDialog.getText(
            self.uiSystem,
            self.uiSystem.MainSystem.lang["ui", "input"],
            self.uiSystem.MainSystem.lang["ui", "input_texture_identifier"],
            text=file_name,
        )
        if not input_[1]:
            return
        identifier = input_[0]
        if (
            identifier
            in self.uiSystem.MainSystem.project_object.resourcePack.terrain_texture[
                "texture_data"
            ]
        ):
            QMessageBox.critical(
                self.uiSystem,
                self.uiSystem.MainSystem.lang["ui", "error"],
                self.uiSystem.MainSystem.lang["ui", "error_repeat"],
            )
            return
        self.uiSystem.MainSystem.project_object.resourcePack.addTexture(
            file_path, identifier
        )
        self.showImportItems()
        self.showComponent()

    def showImportItems(self):
        lib.clearLayout(self.textures_layout)
        # textures
        addon_obj = self.uiSystem.MainSystem.project_object
        img_info = []
        for texture_identifier in addon_obj.resourcePack.terrain_texture[
            "texture_data"
        ]:
            file_path = f"{addon_obj.resourcePack.path}/{addon_obj.resourcePack.terrain_texture['texture_data'][texture_identifier]['textures']}.png"
            img_info.append((texture_identifier, file_path))

        number = int(300 / 100)
        for row in range(0, int(len(img_info) / number) + 1):
            for column in range(max(0, min(len(img_info) - row * number, number))):
                identifier, file_path = img_info[row * number + column]
                layout = QtWidgets.QVBoxLayout()
                layout.setObjectName("layout")
                img = QtWidgets.QLabel(self.textrues_scrollAreaWidgetContents)
                img.setObjectName("img")
                img.setAlignment(Qt.AlignCenter)
                png = QtGui.QPixmap(file_path).scaled(65, 65)
                img.setPixmap(png)
                layout.addWidget(img)
                identifier_label = QtWidgets.QLabel(
                    self.textrues_scrollAreaWidgetContents
                )
                identifier_label.setObjectName("identifier")
                identifier_label.setAlignment(Qt.AlignCenter)
                identifier_label.setText(identifier)
                layout.addWidget(identifier_label)
                self.textures_layout.addLayout(layout, row, column, 1, 1)
        width = number * 100
        if len(img_info) < number:
            width = len(img_info) * 100
        row = len(img_info) / number
        if len(img_info) % number > 0:
            row += 1
        self.textrues_scrollAreaWidgetContents.setGeometry(
            0, 0, int(width), int(row * 90)
        )

    def deleteImportItem(self):
        addon_obj = self.uiSystem.MainSystem.project_object
        textures_identifier = [
            identifier
            for identifier in addon_obj.resourcePack.terrain_texture["texture_data"]
        ]
        input_ = QInputDialog.getItem(
            self.uiSystem,
            self.uiSystem.MainSystem.lang["ui", "input"],
            self.uiSystem.MainSystem.lang["ui", "want_delete"],
            textures_identifier,
            editable=False,
        )
        if not input_[1]:
            return
        addon_obj.resourcePack.deleteTexture(input_[0])
        self.showImportItems()
        self.showComponent()

    def eventTabChanged(self):
        if self.event_tab.currentIndex() == 0:
            return

        self.event_tab.setCurrentIndex(0)
        content = self.getSelectContent()
        if content is None:
            return
        content_type, content = content
        self.uiSystem.showDialog(AskEvents(content.events,content.getEvent(),content))


class AddonSetting(addon_setting.Ui_MainWindow, UiBasic):
    def __init__(self, last_ui):
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
        self.choose_main_version.addItems(
            self.uiSystem.MainSystem.bedrock_game_version_list.keys()
        )
        self.choose_main_version.setCurrentIndex(0)
        self.icon.setPixmap(QtGui.QPixmap(self.icon_path))

    def bind(self):
        self.Cancel.clicked.connect(lambda: self.uiSystem.changeUi(self.last_ui))
        self.random_namepace.clicked.connect(self.randomNamespace)
        self.choose_main_version.currentTextChanged.connect(self.mainVersionChanged)
        self.choose_icon.clicked.connect(self.chooseIcon)
        self.Ok.clicked.connect(self.OK)

    def rename(self):
        self.uiSystem.setWindowTitle(
            self.uiSystem.MainSystem.lang["ui", "addon_setting_title"]
        )
        self.description_label_2.setText(
            self.uiSystem.MainSystem.lang["ui", "description"]
        )
        self.namespace_label.setText(self.uiSystem.MainSystem.lang["ui", "namespace"])
        self.random_namepace.setText(self.uiSystem.MainSystem.lang["ui", "random"])
        self.packName_label.setText(self.uiSystem.MainSystem.lang["ui", "packname"])
        self.pack_version_label.setText(
            self.uiSystem.MainSystem.lang["ui", "pack_version"]
        )
        self.label_4.setText(".")
        self.label_3.setText(".")
        self.game_version_label.setText(
            self.uiSystem.MainSystem.lang["ui", "game_minimum_version"]
        )
        self.icon_label.setText(self.uiSystem.MainSystem.lang["ui", "pack_icon"])
        self.choose_icon.setText(self.uiSystem.MainSystem.lang["ui", "choose"])
        self.Ok.setText(self.uiSystem.MainSystem.lang["ui", "ok"])
        self.Cancel.setText(self.uiSystem.MainSystem.lang["ui", "cancel"])

    def mainVersionChanged(self):
        self.choose_detailed_version.clear()
        self.choose_detailed_version.addItems(
            self.uiSystem.MainSystem.bedrock_game_version_list[
                self.choose_main_version.currentText()
            ]
        )
        self.choose_detailed_version.setCurrentIndex(0)

    def close(self):
        self.uiSystem.changeUi(self.last_ui)

    def randomNamespace(self):
        namespace = ""
        for i in range(5):
            namespace += chr(randint(97, 97 + 26 - 1))
        self.namespace_2.setText(namespace)

    def chooseIcon(self):
        path = QFileDialog.getOpenFileName(self.uiSystem)
        if path[0] != "":
            self.icon_path = path[0]
            self.icon.setPixmap(QtGui.QPixmap(self.icon_path))

    def OK(self):
        if self.check():
            self.uiSystem.MainSystem.project_object = addon.BedrockAddon(
                self.uiSystem.MainSystem
            )
            self.uiSystem.MainSystem.project_object.new(
                "./tmp",
                2,
                self.packName.text(),
                self.description.toPlainText(),
                self.namespace_2.text(),
                [
                    int(self.pack_version_0.text()),
                    int(self.pack_version_1.text()),
                    int(self.pack_version_2.text()),
                ],
                [
                    int(number)
                    for number in self.choose_detailed_version.currentText().split(".")
                ],
            )
            self.uiSystem.MainSystem.project_object.setPackIcon(self.icon_path)
            self.uiSystem.changeUi(AddonUi())

    def check(self):
        blank = []
        if self.packName.text() == "":
            blank.append(self.uiSystem.MainSystem.lang["ui", "packname"])
        if self.namespace_2.text() == "":
            blank.append(self.uiSystem.MainSystem.lang["ui", "namespace"])
        if not blank:
            return True

        message = f"{self.uiSystem.MainSystem.lang['ui','cannot_leave_blank']}\n("
        for name in blank:
            message += name
            message += ","
        message = message[:-1] + ")"
        QMessageBox.critical(
            self.uiSystem, self.uiSystem.MainSystem.lang["ui", "error"], message
        )
        return False


class AskComponent(ask_components.Ui_Dialog, UiBasic):
    def __init__(self, component_dict, callback_func):
        super().__init__()
        self.component_dict = component_dict
        self.callback_func = callback_func

    def showComponents(self, component_dict=None):
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
            self.tableWidget.setRowHeight(row, 70)
            component_info = component_dict[component_identifier]
            new_item = QtWidgets.QTableWidgetItem(component_info["name"])
            new_item.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.tableWidget.setItem(row, 0, new_item)
            description = QtWidgets.QTextBrowser()
            description.setObjectName("description")
            self.tableWidget.setCellWidget(row, 1, description)
            enable = QtWidgets.QCheckBox()
            enable.setObjectName("enable")
            enable.component_identifier = component_identifier
            enable.stateChanged.connect(lambda: self.enableStateChanged(enable))
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
        item.setText(self.ui_system.MainSystem.lang["ui", "name"])
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(self.ui_system.MainSystem.lang["ui", "description"])
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(self.ui_system.MainSystem.lang["ui", "enable"])

    def rename(self):
        self.dialog.setWindowTitle(
            self.ui_system.MainSystem.lang["ui", "ask_component_title"]
        )
        self.search.setPlaceholderText(self.ui_system.MainSystem.lang["ui", "search"])
        self.ok_button.setText(self.ui_system.MainSystem.lang["ui", "ok"])
        self.cancel_button.setText(self.ui_system.MainSystem.lang["ui", "cancel"])
        self.tableRename()

    def bind(self):
        self.cancel_button.clicked.connect(self.dialog.close)
        # self.DialogButtonBox.accepted.connect(self.ok) # 这样写点击按钮没反应
        self.ok_button.clicked.connect(lambda: self.ok())  # 但是这样写可以
        self.search.textChanged.connect(self.searchTextChanged)

    def ok(self):
        component_enable = {}
        for identifier in self.component_dict:
            component_enable[identifier] = self.component_enable_ui[
                identifier
            ].isChecked()
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

    def setupUi(self, ui_system, Dialog):
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

    def enableStateChanged(self, enable):
        self.component_dict[enable.component_identifier][
            "is_checked"
        ] = enable.isChecked()


class Setting(setting.Ui_Dialog, UiBasic):
    def setupUi(self, ui_system, Dialog):
        self.dialog = Dialog
        self.ui_system = ui_system
        super(Setting, self).setupUi(Dialog)

    def rename(self):
        self.dialog.setWindowTitle(
            self.ui_system.MainSystem.lang["ui", "setting_title"]
        )
        self.Individuation.setTitle(
            self.ui_system.MainSystem.lang["ui", "individuation"]
        )
        self.theme_text.setText(self.ui_system.MainSystem.lang["ui", "theme"])
        self.language_text.setText(self.ui_system.MainSystem.lang["ui", "language"])
        self.Update.setTitle(self.ui_system.MainSystem.lang["ui", "update"])
        self.c_v_text.setText(self.ui_system.MainSystem.lang["ui", "current_version"])
        self.c_v.setText("")
        self.l_v_text.setText(self.ui_system.MainSystem.lang["ui", "latest_version"])
        self.l_v.setText("")
        self.check_n_v.setText(
            self.ui_system.MainSystem.lang["ui", "check_new_version"]
        )
        self.Other.setTitle(self.ui_system.MainSystem.lang["ui", "other"])
        self.clear_cache.setText(self.ui_system.MainSystem.lang["ui", "clear_cache"])

    def bind(self):
        self.clear_cache.clicked.connect(lambda: lib.clearFolder("tmp"))
        self.language.currentTextChanged.connect(lambda: self.languageChanged())
        self.theme.currentTextChanged.connect(lambda: self.themeChanged())

    def init(self):
        self.language.clear()
        self.theme.clear()
        self.languages = {}
        for folder in listdir("lang"):
            languages_info = {}
            self.languages[folder] = {}
            with open(f"./lang/{folder}/language", "r", encoding="utf-8") as f:
                for line in f.readlines():
                    line = line[:-1]
                    if "=" not in line:
                        continue
                    key, value = line.split("=")
                    languages_info[key] = value
                    self.languages[folder][key] = value
            self.language.addItem(languages_info["name"])

        for file in listdir("theme"):
            theme_name = file.replace(".qss", "")
            self.theme.addItem(theme_name)
        self.theme.setCurrentText(self.ui_system.MainSystem.config["theme"])

        self.language.setCurrentText(
            self.languages[self.ui_system.MainSystem.config["lang"]]["name"]
        )
        self.rename()
        self.bind()

    def languageChanged(self):
        language = self.language.currentText()
        for lang_id in self.languages:
            if self.languages[lang_id]["name"] == language:
                self.ui_system.MainSystem.loadLanguage(lang_id)
                self.ui_system.ui.rename()
                for ui in self.ui_system.dialog_ui_list:
                    ui.rename()
                self.ui_system.MainSystem.config["lang"] = lang_id
                return

    def themeChanged(self):
        theme = self.theme.currentText()
        self.ui_system.loadTheme(theme)


class AskList(ask_list.Ui_Dialog, UiBasic):
    def __init__(self, list_name="List", list_=None, callback=None):
        if list_ is None:
            list_ = []
        self.list = list_
        self.ui_list = []
        self.list_name = list_name
        self.callback = callback

    def setupUi(self, ui_system, Dialog):
        self.dialog = Dialog
        self.ui_system = ui_system
        super(AskList, self).setupUi(self.dialog)

    def showItems(self):
        self.table.clear()
        self.table.setColumnCount(2)
        self.table.setRowCount(len(self.list))

        for i in range(2):
            self.table.setHorizontalHeaderItem(i, QtWidgets.QTableWidgetItem())
        self.ui_list = []
        for index in range(len(self.list)):
            item = self.list[index]
            item_type = QtWidgets.QComboBox(self.table)
            item_type.addItems(["int", "bool", "str"])
            if isinstance(item, bool):
                widget = QtWidgets.QCheckBox(self.table)
                widget.setChecked(item)
                widget.clicked.connect(self.widgetChanged)
                item_type.setCurrentText("bool")
            elif isinstance(item, int):
                widget = QtWidgets.QSpinBox(self.table)
                widget.setValue(item)
                widget.setMaximum(10000000)
                widget.setMinimum(-10000000)
                widget.valueChanged.connect(self.widgetChanged)
                item_type.setCurrentText("int")
            else:
                widget = QtWidgets.QLineEdit(self.table)
                widget.setText(item)
                widget.textChanged.connect(self.widgetChanged)
                item_type.setCurrentText("str")
            item_type.currentTextChanged.connect(self.typeChanged)
            self.table.setCellWidget(index, 0, widget)
            self.table.setCellWidget(index, 1, item_type)
            self.ui_list.append((widget, item_type))
        self.tableRename()

    def init(self):
        self.table.verticalHeader().hide()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.Interactive | QHeaderView.Stretch
        )
        self.showItems()
        self.rename()
        self.bind()

    def rename(self):
        self.dialog.setWindowTitle(self.list_name)

    def bind(self):
        self.add.clicked.connect(self.addItem)
        self.remove.clicked.connect(self.removeItem)
        self.dialog_button.accepted.connect(self.ok)
        self.dialog_button.rejected.connect(self.cancel)
        self.up.clicked.connect(self.itemUp)
        self.down.clicked.connect(self.itemDown)

    def tableRename(self):
        self.table.horizontalHeaderItem(0).setText(
            self.ui_system.MainSystem.lang["ui", "list_value"]
        )
        self.table.horizontalHeaderItem(1).setText(
            self.ui_system.MainSystem.lang["ui", "list_value_type"]
        )

    def typeChanged(self):
        for index in range(len(self.ui_list)):
            widget, value_type_combobox = self.ui_list[index]
            value = lib.getWidgetValue(widget)
            value_type = "str"
            if isinstance(value, bool):
                value_type = "bool"
            elif isinstance(value, int):
                value_type = "int"
            if value_type != value_type_combobox.currentText():
                new_type = value_type_combobox.currentText()
                self.list[index] = ""
                if new_type == "bool":
                    self.list[index] = False
                elif new_type == "int":
                    self.list[index] = 0
                break
        self.showItems()

    def addItem(self):
        self.list.append(0)
        self.showItems()

    def removeItem(self):
        if len(self.list) == 0:
            return
        index = self.table.currentRow()
        self.list.pop(index)
        self.showItems()

    def ok(self):
        if self.callback is None:
            return
        self.callback("list", list_name=self.list_name, list_=self.list)
        self.dialog.close()

    def itemUp(self):
        index = self.table.currentRow()
        value = self.list[index]
        new_index = index - 1
        if new_index == -1:
            new_index = len(self.list) - 1
        self.list.pop(index)
        self.list.insert(new_index, value)
        self.showItems()
        self.table.setCurrentCell(new_index, 0)

    def itemDown(self):
        index = self.table.currentRow()
        value = self.list[index]
        new_index = index + 1
        if new_index == len(self.list):
            new_index = 0
        self.list.pop(index)
        self.list.insert(new_index, value)
        self.showItems()
        self.table.setCurrentCell(new_index, 0)

    def cancel(self):
        self.dialog.close()

    def widgetChanged(self):
        return_list = []
        for index in range(len(self.ui_list)):
            widget, value_type_combobox = self.ui_list[index]
            return_list.append(lib.getWidgetValue(widget))
        self.list = return_list


class AskEvents(ask_events.Ui_Dialog, UiBasic):
    def __init__(self, events,event_data,content):
        self.events = events
        self.event_data = event_data
        self.ui = {}
        self.content = content
        super(AskEvents, self).__init__()

    def rename(self):
        self.dialog.setWindowTitle(self.ui_system.MainSystem.lang["ui","event_response"])
        self.groupBox.setTitle(self.ui_system.MainSystem.lang["ui","events"])

    def bind(self):
        self.add_events.clicked.connect(self.addEvent)
        self.remove_events.clicked.connect(self.removeEvent)
        self.events_list.currentItemChanged.connect(self.updateEventResponse)
        self.events_list.setCurrentRow(0)
        self.buttonBox.accepted.connect(self.ok)
        self.buttonBox.rejected.connect(self.dialog.close)
        self.set_event_response.clicked.connect(self.setEventResponses)

    def init(self):
        self.rename()
        self.showEventList()
        self.bind()

    def setupUi(self, ui_system, Dialog):
        self.dialog = Dialog
        self.ui_system = ui_system
        super(AskEvents, self).setupUi(self.dialog)

    def showEventList(self):
        events = [event for event in self.events.keys()]
        self.events_list.clear()
        self.events_list.addItems(events)

    def updateEventResponse(self):
        lib.clearLayout(self.event_data_layout)
        data = self.getSelectEventDict()
        if data is None:
            return
        size = 20
        self.ui = {}
        for response_identifier in data:
            group_box = QtWidgets.QGroupBox(self.scrollAreaWidgetContents)
            group_box.setObjectName("groupBox")
            group_box.setTitle(self.ui_system.MainSystem.lang["addon",f"{response_identifier}_name"])
            form_layout = QtWidgets.QFormLayout(group_box)
            form_layout.setObjectName("formLayout")
            self.ui[response_identifier], s = self.ui_system.MainSystem.setDataUi(
                group_box, form_layout, data[response_identifier].getUiDict(), response_identifier, "event", self.dataChanged
            )
            size += s
            self.event_data_layout.addWidget(group_box)
        self.scrollAreaWidgetContents.setGeometry(0, 0, 260, size)

    def dataChanged(self, item_type, **args):
        if self.events_list.currentItem() is None:
            return
        item = args["item"]
        ui_dict = self.ui[item.identifier]
        self.events[self.events_list.currentItem().text()][item.identifier].parseFromUi(
            ui_dict
        )

    def addEvent(self):
        identifier,flag = QInputDialog.getText(self.ui_system,self.ui_system.MainSystem.lang["ui","input"],self.ui_system.MainSystem.lang["ui","input_event_identifier"])
        if not flag:
            return
        if identifier == "":
            QMessageBox.critical(self.ui_system,self.ui_system.MainSystem.lang["ui","error"],self.ui_system.MainSystem.lang["ui","cannot_leave_blank"])
        self.events[identifier] = {}
        self.showEventList()

    def removeEvent(self):
        index = self.events_list.currentIndex().row()
        if index == -1:
            return
        event_identifier = self.events_list.item(index).text()
        self.events.pop(event_identifier)
        self.showEventList()

    def getSelectIdentifier(self):
        if self.events_list.currentItem() is None:
            return None
        event_identifier = self.events_list.currentItem().text()
        return event_identifier

    def getSelectEventDict(self):
        event_identifier = self.getSelectIdentifier()
        if event_identifier is None:
            return None
        return self.events[event_identifier]

    def ok(self):
        self.content.events = self.events
        self.dialog.close()

    def responsesChanged(self, response_enable_list):
        identifier = self.getSelectIdentifier()
        event = self.getSelectEventDict()
        for identifier in response_enable_list:
            if response_enable_list[identifier] and identifier not in event:
                event[identifier] = BlockEventResponses.responses[identifier](self.content,self.ui_system,self.getSelectIdentifier())
            elif not response_enable_list[identifier] and identifier in event:
                event.pop(identifier)
        self.events[identifier] = event
        self.updateEventResponse()

    def setEventResponses(self):
        event_data = self.event_data
        event = self.getSelectEventDict()
        for identifier in event_data:
            if identifier in event:
                event_data[identifier]["is_checked"] = True
            else:
                event_data[identifier]["is_checked"] = False
        dialog = AskComponent(event_data, self.responsesChanged)
        self.ui_system.showDialog(dialog)
        dialog.showComponents()


class UiSystem(QMainWindow):
    def __init__(self, MainSystem, Ui=StartUi()):
        super().__init__()
        self.MainSystem = MainSystem
        self.ui = None
        self.dialog_list = []
        self.dialog_ui_list = []
        self.style_sheet = None
        self.setAcceptDrops(False)
        self.loadTheme(self.MainSystem.config["theme"])
        self.changeUi(Ui)

    def loadTheme(self, theme):
        self.MainSystem.config["theme"] = theme
        if f'{self.MainSystem.config["theme"]}.qss' not in listdir("theme"):
            self.MainSystem.config["theme"] = "Default"
        with open(f"./theme/{self.MainSystem.config['theme']}.qss") as f:
            self.style_sheet = f.read()
        self.setStyleSheet(self.style_sheet)

    def changeUi(self, ui_obj):
        self.ui = ui_obj
        self.ui.setupUi(self)
        self.ui.init()
        self.setAcceptDrops(self.ui.drop_callback)

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.ui.close_callback:
            event.ignore()
            self.ui.close()

    def showDialog(self, ui_obj):
        while len(self.dialog_list) >= 5:
            self.dialog_list[0].close()
        self.dialog_ui_list.append(ui_obj)
        self.dialog_list.append(lib.Dialog(self, self.dialog_list, self.dialog_ui_list))
        self.dialog_ui_list[-1].setupUi(self, self.dialog_list[-1])
        self.dialog_ui_list[-1].init()
        self.dialog_list[-1].show()

    def dragEnterEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        self.ui.drop(event.mimeData().text())
