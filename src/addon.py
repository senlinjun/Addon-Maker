# Bedrock
import time
import uuid
import json
from lib import *


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
        for identifier in self.addon.blocks:
            block = self.addon.blocks[identifier]
            block_id = block.id
            block_data = block.behavior_data
            block_namespace = block.namespace
            with open(f"{self.path}/blocks/{block_namespace}_{block_id}.json", "w") as f:
                json.dump(block_data, f, indent=1)

    def load(self):
        with open(f"{self.path}/manifest.json", "r") as f:
            self.manifest = json.load(f)
        for file_name in os.listdir(f"{self.path}/blocks"):
            with open(f"{self.path}/blocks/{file_name}","r") as f:
                block_data = json.load(f)
            id = block_data["minecraft:block"]["description"]["identifier"].split(":")[1]
            self.addon.blocks[f"{self.addon.namespace}:{id}"] = Block(self.addon)
            self.addon.blocks[f"{self.addon.namespace}:{id}"].namespace = self.addon.namespace
            self.addon.blocks[f"{self.addon.namespace}:{id}"].id = id
            self.addon.blocks[f"{self.addon.namespace}:{id}"].behavior_data = f"{self.addon.namespace}:{id}"
            self.addon.blocks[f"{self.addon.namespace}:{id}"].behavior_data = block_data


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
            blocks_json[block.identifier] = block.blocks_value
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
            block.namespace_identifier = identifier
            block.blocks_value = blocks_data[identifier]

        # lang
        with open(f"{self.path}/texts/{self.lang}.lang", "r", encoding="utf-8") as f:
            for line in f.readlines():
                key,value = line.split("=")
                identifier = key.split(".")[1]
                self.addon.blocks[identifier].name = value


class Block:
    def __init__(self, addon):
        self.addon = addon
        self.namespace = ""
        self.id = ""
        self.behavior_data = {}
        self.blocks_value = {}
        self.name = ""
        self.identifier = ""

    def new(self, id):
        self.namespace = self.addon.namespace
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
        self.blocks_value = {}

    def setName(self, name):
        # tile.demo:die.name=Die
        # self.ResourcePack.lang["lang"][f"tile.{self.namespace}:{self.identifier}.name"] = name
        self.name = name

    def setResourceData(self, texture_id: str, brightness: int, sound: str, isotropic: bool, carried_texture_id=None):
        self.namespace_identifier = f"{self.namespace}:{self.id}"
        self.blocks_value = {
            "textures": texture_id,
            "isotropic": isotropic,
            "brightness_gamma": brightness,
            "sound": sound
        }
        if carried_texture_id is not None:
            self.blocks_value["carried_textures"] = carried_texture_id

    def addComponent(self, key, value):
        self.behavior_data["components"][key] = value

    def removeComponent(self, key):
        self.behavior_data["components"].pop(key)


class BedrockAddon:
    def __init__(self):
        self.packname = ""
        self.description = ""
        self.namespace = ""
        self.pack_version = [1,0,0]
        self.min_engine_version = [1,0,0]
        self.blocks = {}
        self.path = ""
        self.behaviorPack = None
        self.resourcePack = None

    def new(self, path: str, format_version: int, packname: str, description: str, namespace: str, pack_version:list, min_engine_version:list):
        self.packname = packname
        self.description = description
        self.namespace = namespace
        self.pack_version = pack_version
        self.min_engine_version = min_engine_version
        path = path + f"/{packname}"
        self.path = path

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
        self.buildDirectories()

        self.blocks = {}

    def save(self):
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
        with open(f"./works/{self.packname}/project.json","w",encoding="utf-8") as f:
            json.dump(data,f,indent=1)
        self.behaviorPack.save()
        self.resourcePack.save()

    def load(self,path,data):
        self.path = path + f"/{data['pack_data']['name']}"
        self.packname, self.description, self.namespace, self.pack_version, self.min_engine_version = data["pack_data"]["name"], data["pack_data"]["description"], data["pack_data"]["namespace"], data["pack_data"]["pack_version"], data["pack_data"]["min_engine_version"]
        self.behaviorPack = BehaviorPack(self,self.path)
        self.resourcePack = ResourcePack(self, self.path)
        self.behaviorPack.load()
        self.resourcePack.load()
        print(self.blocks)

    def buildDirectories(self):
        os.mkdir(f"./works/{self.packname}")
        with open("./directories.json", "r") as f:
            directories = json.load(f)
        buildDirectories(f"./works/{self.packname}", directories)

if __name__ == "__main__":
    test = BedrockAddon()
    test.new("./works", 2, "packName", "packIntroduce", "namespace",[1,0,0],[1,19,30])
    b = Block(test)
    test.blocks["namespace:newBlock"] = b
    b.new("newBlock")
    b.setName("NewBlock")
    test.resourcePack.addBlockTexture("./resources/test.png")
    b.setResourceData("test", 1, "sand", True)
    test.save()

    test = BedrockAddon()
    with open("./works/packName/project.json","r") as f:
        data = json.load(f)
    test.load("./works",data)
    b = Block(test)
    test.blocks["namespace:newBlock1"] = b
    b.new("newBlock1")
    b.setName("NewBlock1")
    b.setResourceData("test", 1, "stone", True)
    test.save()
