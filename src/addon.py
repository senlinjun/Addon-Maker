# Bedrock
import time
import uuid
import json
import zipfile
from lib import *
from data.addon import BlockBehavior


class BehaviorPack:
    def __init__(self, addon, path):
        path = path + f"/behavior_pack"
        self.path = path
        self.addon = addon
        self.pack_name = ""
        self.manifest = {}

    def new(self, pack_name: str, manifest: dict):
        self.pack_name = pack_name
        self.manifest = manifest

    def save(self):
        with open(f"{self.path}/manifest.json", "w") as f:
            json.dump(self.manifest, f, indent=1)

        # Blocks
        clearFolder(f"{self.path}/blocks")
        for identifier in self.addon.blocks:
            block = self.addon.blocks[identifier]
            block_id = block.id
            block.generateBehaviorData()
            block_data = block.behavior_data
            print(block_data)
            block_namespace = block.namespace
            with open(f"{self.path}/blocks/{block_namespace}_{block_id}.json", "w") as f:
                json.dump(block_data, f, indent=1)

    def load(self):
        with open(f"{self.path}/manifest.json", "r") as f:
            self.manifest = json.load(f)

        # Blocks
        for file_name in os.listdir(f"{self.path}/blocks"):
            with open(f"{self.path}/blocks/{file_name}","r") as f:
                block_data = json.load(f)
            namespace,id = block_data["minecraft:block"]["description"]["identifier"].split(":")
            self.addon.blocks[f"{namespace}:{id}"] = Block(self.addon)
            block = self.addon.blocks[f"{namespace}:{id}"]
            block.namespace = namespace
            block.id = id
            block.behavior_data = f"{namespace}:{id}"
            block.behavior_data = block_data
            for component in ["is_experimental","register_to_creative_menu"]:
                if component in BlockBehavior.components:
                    block.addBehaviorComponent(component)
            for component in block_data["minecraft:block"]["components"]:
                if component in BlockBehavior.components:
                    component_obj = BlockBehavior.components[component]()
                    component_obj.parse(block_data["minecraft:block"]["components"][component])
                    block.components[component] = component_obj


class ResourcePack:
    def __init__(self, addon, path):
        path = path + f"/resource_pack"
        self.path = path
        self.addon = addon
        self.pack_name = ""
        self.manifest = {}
        self.lang = ""
        self.terrain_texture = {}

    def new(self, pack_name: str, manifest: dict):
        self.pack_name = pack_name
        self.manifest = manifest
        self.lang = "zh_CN"
        self.terrain_texture = {
            "resource_pack_name": self.pack_name,
            "texture_name": "atlas.terrain",
            "padding": 8,
            "num_mip_levels": 4,
            "texture_data": {}
        }

    def addBlockTexture(self, file: str):
        filename = file.split("/")[-1].split("\\")[-1].replace(".png", "")
        with open(file, "rb") as f:
            data = f.read()
        with open(f"{self.path}/textures/blocks/{filename}.png", "wb") as f:
            f.write(data)
        self.terrain_texture["texture_data"][filename] = {"textures": f"textures/blocks/{filename}"}

    def save(self):
        lang = {}

        with open(f"{self.path}/manifest.json", "w") as f:
            json.dump(self.manifest, f, indent=1)

        with open(f"{self.path}/textures/terrain_texture.json", "w") as f:
            json.dump(self.terrain_texture, f, indent=1)

        # Blocks
        blocks_json = {
            "format_version": "1.19.30"
        }
        for identifier in self.addon.blocks:
            block = self.addon.blocks[identifier]
            blocks_json[block.identifier] = block.resource_data
            if block.name is not None:
                lang[f"tile.{identifier}.name"] = block.name
        with open(f"{self.path}/blocks.json", "w") as f:
            json.dump(blocks_json, f, indent=1)

        # lang
        with open(f"{self.path}/texts/{self.lang}.lang", "w", encoding="utf-8") as f:
            for key in lang:
                f.write(f"{key}={lang[key]}\n")

    def load(self):
        self.lang = "zh_CN"
        with open(f"{self.path}/manifest.json", "r") as f:
            self.manifest = json.load(f)

        with open(f"{self.path}/textures/terrain_texture.json", "r") as f:
            self.terrain_texture = json.load(f)

        # Blocks
        with open(f"{self.path}/blocks.json", "r") as f:
            blocks_data = json.load(f)
        for identifier in self.addon.blocks:
            block = self.addon.blocks[identifier]
            block.identifier = identifier
            block.resource_data = blocks_data[identifier]

        # lang
        with open(f"{self.path}/texts/{self.lang}.lang", "r", encoding="utf-8") as f:
            for line in f.readlines():
                line = line.replace("\n", "")
                line = line.replace("\r", "")
                if line == "":
                    continue
                key,value = line.split("=")
                identifier = key.split(".")[1]
                self.addon.blocks[identifier].name = value


class Block:
    def __init__(self, addon):
        self.addon = addon
        self.namespace = ""
        self.id = ""
        self.behavior_data = {}
        self.resource_data = {}
        self.components = {}
        self.name = None
        self.identifier = ""

    def new(self, namespace, id):
        self.namespace = namespace
        self.id = id
        self.identifier = f"{self.namespace}:{self.id}"
        self.behavior_data = {
            "format_version": "1.19.30",
            "minecraft:block": {
                "description": {
                    "identifier": f"{self.namespace}:{self.id}"
                },
                "components": {
                }
            }
        }
        self.resource_data = {}

    def remove(self):
        self.addon.blocks.pop(self.identifier)

    def generateBehaviorData(self):
        self.behavior_data = {
            "format_version": "1.19.30",
            "minecraft:block": {
                "description": {
                    "identifier": f"{self.namespace}:{self.id}"
                },
                "components": {
                }
            }
        }
        for component_identifier in self.components:
            component = self.components[component_identifier]
            component.write(self.behavior_data)


    # TODO Resource

    def getBehaviorComponents(self):
        back_dict = {}
        for component in BlockBehavior.components:
            back_dict[component] = {
                "name":self.addon.MainSystem.lang["addon"][f"{component}_name"],
                "description": self.addon.MainSystem.lang["addon"][f"{component}_description"],
                "is_checked": component in self.components
            }
        return back_dict

    def addBehaviorComponent(self,component_identifier):
        self.components[component_identifier] = BlockBehavior.components[component_identifier]()

    def removeBehaviorComponent(self,component_identifier):
        self.components.pop(component_identifier)

class BedrockAddon:
    def __init__(self,MainSystem):
        self.packname = ""
        self.description = ""
        self.namespace = ""
        self.pack_version = [1,0,0]
        self.min_engine_version = [1,0,0]
        self.blocks = {}
        self.path = ""
        self.save_path = None
        self.behaviorPack = None
        self.resourcePack = None
        self.MainSystem = MainSystem

    def new(self, path: str, format_version: int, packname: str, description: str, namespace: str, pack_version:list, min_engine_version:list):
        self.packname = packname
        self.description = description
        self.namespace = namespace
        self.pack_version = pack_version
        self.min_engine_version = min_engine_version
        path = path + f"/{packname}"
        self.path = path

        self.buildDirectories()

        self.behaviorPack = BehaviorPack(self, self.path)
        self.resourcePack = ResourcePack(self, self.path)

        resource_uuid = str(uuid.uuid4())
        self.behaviorPack.new(
            packname,
            {
                "format_version": 2,
                "header": {
                    "description": description,
                    "name": packname,
                    "uuid": str(uuid.uuid4()),
                    "version": self.pack_version,
                    "min_engine_version": [1, 19, 20]
                },
                "modules": [
                    {
                        "description": description,
                        "type": "data",
                        "uuid": str(uuid.uuid4()),
                        "version": self.pack_version
                    }
                ],
                "dependencies": [
                    {
                        "uuid": resource_uuid,
                        "version": self.pack_version
                    }
                ]
            }
        )
        self.resourcePack.new(
            packname,
            {
                "format_version": 2,
                "header": {
                    "description": description,
                    "name": packname,
                    "uuid": resource_uuid,
                    "version": self.pack_version,
                    "min_engine_version": [1, 19, 20]
                },
                "modules": [
                    {
                        "description": description,
                        "type": "resources",
                        "uuid": str(uuid.uuid4()),
                        "version": self.pack_version
                    }
                ]
            }
        )

        self.blocks = {}

    def saveToDir(self):
        data = {
            "pack_type":"addon",
            "modification_time":time.time(),
            "pack_data":{
                "name":self.packname,
                "description":self.description,
                "namespace":self.namespace,
                "pack_version":self.pack_version,
                "min_engine_version":self.min_engine_version,
                "format_version":2
            }
        }
        with open(f"./tmp/{self.packname}/project.json","w",encoding="utf-8") as f:
            json.dump(data,f,indent=1)
        self.behaviorPack.save()
        self.resourcePack.save()

    def save(self):
        self.saveToDir()
        zip = zipfile.ZipFile(self.save_path,"w")
        compressDir(self.path,zip,self.packname)
        zip.close()

    def load(self,path,data):
        self.path = path
        self.packname, self.description, self.namespace, self.pack_version, self.min_engine_version = data["pack_data"]["name"], data["pack_data"]["description"], data["pack_data"]["namespace"], data["pack_data"]["pack_version"], data["pack_data"]["min_engine_version"]
        self.behaviorPack = BehaviorPack(self,self.path)
        self.resourcePack = ResourcePack(self, self.path)
        self.behaviorPack.load()
        self.resourcePack.load()

    def buildDirectories(self):
        os.mkdir(f"./tmp/{self.packname}")
        with open("data/addon/directories.json", "r") as f:
            directories = json.load(f)
        buildDirectories(f"./tmp/{self.packname}", directories)

    def export(self,path):
        behavior_zip = zipfile.ZipFile(f"{path}/{self.packname}-behavior.mcpack","w")
        compressDir(self.behaviorPack.path,behavior_zip)
        behavior_zip.close()
        resource_zip = zipfile.ZipFile(f"{path}/{self.packname}-resource.mcpack", "w")
        compressDir(self.resourcePack.path, resource_zip)
        resource_zip.close()

    def setPackIcon(self,path):
        with open(path,"rb") as f:
            img = f.read()
        with open(f"{self.behaviorPack.path}/pack_icon.png","wb") as f:
            f.write(img)
        with open(f"{self.resourcePack.path}/pack_icon.png","wb") as f:
            f.write(img)

    def close(self):
        clearFolder("tmp")
