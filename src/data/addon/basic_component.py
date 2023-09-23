from PyQt5.QtCore import Qt


class BasicComponent:
    def __init__(self, identifier, content, ui_system):
        self.identifier = identifier
        self.content = content
        self.ui_system = ui_system
        self.lang = self.content.addon.MainSystem.lang

    def parse(self, component_value):
        pass

    def generate(self):
        pass

    def write(self, pack_dict):
        pass

    def getUiDict(self):
        pass

    def parseFromUi(self, ui_dict):
        pass

    def updateUi(self, ui, data):
        if isinstance(ui, dict):
            for key in ui:
                self.updateUi(ui[key], data[key])
            return

        value, value_type, args = data
        if value_type == "bool":
            ui.setChecked(value)

        elif value_type == "int":
            if args is not None:
                ui.setMinimum(args[0])
                ui.setMaximum(args[1])
                if len(args) >= 3:
                    ui.setSingleStep(args[2])
            ui.setValue(value)

        elif value_type == "float":
            if args is not None:
                ui.setMinimum(args[0])
                ui.setMaximum(args[1])
                if len(args) >= 3:
                    ui.setSingleStep(args[2])
            ui.setValue(value)

        elif value_type == "str":
            if args is not None:
                ui.setMaxLength(args)
            ui.setText(value)

        elif value_type == "combobox":
            if args is not None:
                ui.addItems(args)
                ui.setCurrentText(value)

        elif value_type == "button":
            ui.setText(args)
            ui.clicked.connect(value)

        elif value_type == "list":
            ui.setText(self.lang["ui", "edit"])
            ui.component_list = value

        elif value_type == "tristate":
            ui.setTristate()
            if value == 0:
                ui.setCheckState(Qt.Unchecked)
            elif value == 1:
                ui.setCheckState(Qt.PartiallyChecked)
            elif value == 2:
                ui.setCheckState(Qt.Checked)
