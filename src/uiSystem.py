import random, lib, sys, addon

from ui import start,addonUi,addon_setting
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow, QFileDialog,QMessageBox
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

    def rename(self):
        _translate = QtCore.QCoreApplication.translate
        self.uiSystem.setWindowTitle(_translate("Form", "Form"))
        self.new_addon.setText(_translate("Form", "New Bedrock Addon"))
        self.new_mod.setText(_translate("Form", "New Java Mod"))
        self.open.setText(_translate("Form", "Open"))
        self.setting.setText(_translate("Form", "setting"))
        self.recent.setTitle(_translate("Form", "recent"))

    def bind(self):
        self.new_addon.clicked.connect(lambda:self.uiSystem.changeUi(AddonSetting(self)))

class AddonUi(addonUi.Ui_MainWindow, UiBasic):
    def setupUi(self, uiSystem):
        super().setupUi(uiSystem)
        self.uiSystem = uiSystem

class AddonSetting(addon_setting.Ui_MainWindow,UiBasic):

    def __init__(self,last_ui):
        super().__init__()
        self.last_ui = last_ui

    def setupUi(self, uiSystem):
        super().setupUi(uiSystem)
        self.uiSystem = uiSystem

    def init(self):
        self.icon_path = "./test.png"
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
        self.uiSystem.setWindowTitle(_translate("MainWindow", "MainWindow"))
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
                self.namespace_2.text()
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