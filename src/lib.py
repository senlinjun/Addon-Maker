import os
from requests import get
from lxml import etree
from PyQt5 import QtWidgets

def buildDirectories(path,directories):
    p = os.getcwd()
    os.chdir(path)
    for directory in directories:
        if directory not in os.listdir():
            os.mkdir(directory)
        buildDirectories(directory,directories[directory])
    os.chdir(p)

def getBedrockGameVersionsList():
    g = get("https://minecraft.fandom.com/zh/wiki/%E5%9F%BA%E5%B2%A9%E7%89%88%E7%89%88%E6%9C%AC%E8%AE%B0%E5%BD%95")
    html = etree.HTML(g.text)
    main_versions_list = html.xpath('//div[@class="mw-parser-output"]/h3/span[@class="mw-headline"]/text()')
    detailed_versions_list = html.xpath('//div[@class="mw-parser-output"]/table[@class="wikitable"]/tbody/tr/td[1]/a/text()')
    return_dict = {}
    for version in main_versions_list:
        if version >= "1.0" and version != "Pre-Release":
            return_dict[version] = []
    for version in detailed_versions_list:
        version_list = version.split(".")
        if len(version_list) != 3:
            continue
        main_version = f"{version_list[0]}.{version_list[1]}"
        if main_version in main_versions_list:
            return_dict[main_version].append(version)
    for version in return_dict:
        return_dict[version].append(f"{version}.0")

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
    if isinstance(widget,QtWidgets.QCheckBox):  # bool
        return widget.isChecked()
    if isinstance(widget,QtWidgets.QSpinBox):  # int
        return widget.value()
    if isinstance(widget,QtWidgets.QDoubleSpinBox):  # float
        return widget.value()
    if isinstance(widget,QtWidgets.QLineEdit):  # str
        return widget.text()
    if isinstance(widget,QtWidgets.QTextEdit):  # str
        return widget.toPlainText()


class Language:
    def __init__(self,id):
        self.lang = {}
        self.lang_info = {}
        self.lang_keys = []
        self.loadLangFolder(id)

    def loadLangFolder(self,id):
        self.lang = {}
        self.lang_info = {}
        self.id = id
        for file in os.listdir(f"lang/{id}"):
            if file == "language":
                with open(f"lang/{id}/language","r",encoding="utf-8") as f:
                    for line in f.readlines():
                        line = line[:-1]
                        key,value = line.split("=")
                        self.lang_info[key] = value

            with open(f"lang/{id}/{file}", "r", encoding="utf-8") as f:
                for line in f.readlines():
                    if "=" not in line:
                        continue
                    line = line[:-1]
                    key, value = line.split("=")
                    self.lang[f"{file.replace('.lang','')}_{key}"] = value
        self.lang_keys = self.lang.keys()

    def __getitem__(self,t):
        module,lang_id = t
        if f"{module}_{lang_id}" in self.lang_keys:
            return self.lang[f"{module}_{lang_id}"]
        return f"{module}_{lang_id}"
