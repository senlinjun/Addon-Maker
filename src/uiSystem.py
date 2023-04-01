import random

from ui import start,addon,addon_setting
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QMainWindow
from PyQt5.QtCore import QCoreApplication
import sys

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

class AddonUi(addon.Ui_MainWindow,UiBasic):
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
        self.img_path = ""
        self.rename()
        self.bind()
        self.close_callback = True

    def close(self):
        self.uiSystem.changeUi(self.last_ui)

    def randomNamespace(self):
        namespace = ""
        for i in range(5):
            namespace += chr(random.randint(97,97+26-1))
        self.namespace_2.setText(namespace)

    def bind(self):
        self.Cancel.clicked.connect(lambda:self.uiSystem.changeUi(self.last_ui))
        self.random_namepace.clicked.connect(self.randomNamespace)

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

class UiSystem(QMainWindow):
    def __init__(self,Ui=StartUi()):
        super().__init__()
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

if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainwindow = UiSystem()
    mainwindow.show()
    app.exec_()