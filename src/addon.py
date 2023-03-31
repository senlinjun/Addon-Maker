# Bedrock

import uuid
import json
from lib import *


class BehaviorPack:
    def __init__(self, addon, path):
        path = path + f"/behavior_pack"
        self.path = path
        self.addon = addon
        self.entities = []
        self.items = []
        self.loot_tables = []
        self.recipes = []
        self.spawn_rules = []
        self.trading = []
        self.blocks = []
        self.pack_name = ""
        self.manifest = {}

    def new(self, pack_name: str, manifest: dict):
        self.entities = []
        self.items = []
        self.loot_tables = []
        self.recipes = []
        self.spawn_rules = []
        self.trading = []
        self.blocks = []
        self.pack_name = pack_name
        self.manifest = manifest

    def save(self):
        with open(f"{self.path}/manifest.json", "w") as f:
            json.dump(self.manifest, f, indent=1)

        # Blocks
        for block in self.addon.blocks:
            block_identifier = block.identifier
            block_data = block.behavior_data
            block_namespace = block.namespace
            with open(f"{self.path}/blocks/{block_namespace}_{block_identifier}.json", "w") as f:
                json.dump(block_data, f, indent=1)


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
        for block in self.addon.blocks:
            blocks_json[block.blocks_key] = block.blocks_value
            lang[f"tile.{block.namespace}:{block.identifier}.name"] = block.name
        with open(f"{self.path}/blocks.json", "w") as f:
            json.dump(blocks_json, f, indent=1)

        # lang
        with open(f"{self.path}/texts/{self.lang}.lang", "w", encoding="utf-8") as f:
            for key in lang:
                f.write(f"{key}={lang[key]}\n")


class Block:
    def __init__(self, addon):
        self.addon = addon
        self.namespace = ""
        self.identifier = ""
        self.behavior_data = {}
        self.blocks_value = {}
        self.name = ""
        self.blocks_key = {}

    def new(self, namespace, identifier):
        self.namespace = namespace
        self.identifier = identifier
        self.behavior_data = {
            "format_version": "1.19.30",
            "minecraft:block": {
                "description": {
                    "identifier": f"{self.namespace}:{self.identifier}"
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
        self.blocks_key = f"{self.namespace}:{self.identifier}"
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
        self.blocks = []
        self.path = ""
        self.behaviorPack = None
        self.resourcePack = None

    def new(self, path: str, format_version: int, packname: str, description: str, namespace: str):
        self.packname = packname
        self.description = description
        self.namespace = namespace
        path = path + f"/{packname}"
        self.path = path

        self.behaviorPack = BehaviorPack(self, self.path)
        self.resourcePack = ResourcePack(self, self.path)

        resource_uuid = str(uuid.uuid4())
        self.behaviorPack.new(
            packname,
            {
                "format_version": format_version,
                "header": {
                    "description": description,
                    "name": packname,
                    "uuid": str(uuid.uuid4()),
                    "version": [0, 0, 1],
                    "min_engine_version": [1, 19, 20]
                },
                "modules": [
                    {
                        "description": description,
                        "type": "data",
                        "uuid": str(uuid.uuid4()),
                        "version": [0, 0, 1]
                    }
                ],
                "dependencies": [
                    {
                        "uuid": resource_uuid,
                        "version": [0, 0, 1]
                    }
                ]
            }
        )
        self.resourcePack.new(
            packname,
            {
                "format_version": format_version,
                "header": {
                    "description": description,
                    "name": packname,
                    "uuid": resource_uuid,
                    "version": [0, 0, 1],
                    "min_engine_version": [1, 19, 20]
                },
                "modules": [
                    {
                        "description": description,
                        "type": "resources",
                        "uuid": str(uuid.uuid4()),
                        "version": [0, 0, 1]
                    }
                ]
            }
        )
        self.buildDirectories()

        self.blocks = []

    def save(self):
        self.behaviorPack.save()
        self.resourcePack.save()

    def buildDirectories(self):
        if "works" not in os.listdir():
            os.mkdir("works")
        os.mkdir(f"./works/{self.packname}")
        with open("./directories.json", "r") as f:
            directories = json.load(f)
        buildDirectories(f"./works/{self.packname}", directories)


if __name__ == "__main__":
    test = BedrockAddon()
    test.new("./works", 2, "packName", "packIntroduce", "namespace")
    b = Block(test)
    test.blocks.append(b)
    b.new(test.namespace, "newBlock")
    b.setName("NewBlock")
    test.resourcePack.addBlockTexture("./texture.png")
    b.setResourceData("texture_id", 1, "sound", True)
    test.save()
