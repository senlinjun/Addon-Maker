import os, requests
from lxml import etree

def buildDirectories(path,directories):
    p = os.getcwd()
    os.chdir(path)
    for directory in directories:
        if directory not in os.listdir():
            os.mkdir(directory)
        buildDirectories(directory,directories[directory])
    os.chdir(p)

def getBedrockGameVersionsList():
    get = requests.get("https://minecraft.fandom.com/zh/wiki/%E5%9F%BA%E5%B2%A9%E7%89%88%E7%89%88%E6%9C%AC%E8%AE%B0%E5%BD%95")
    html = etree.HTML(get.text)
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