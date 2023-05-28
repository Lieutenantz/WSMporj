#!/usr/bin/env python3
import os
import json
import hashlib
from functools import lru_cache
import pymongo
from pymongo.collection import Collection
from PIL import Image
import re
import numpy as np

# import clip

@lru_cache(maxsize=1)
def get_config():
    with open("config.json") as json_config:
        conf = json.load(json_config)
    # if "clip-model" in conf:
    #     assert conf["clip-model"] in clip.availble_models()
    # if "device" in conf:
    #     assert conf.device in ["cuda", "cpu"]
    return conf

def get_file_type(image_path):
    libmagic_output = os.popen("file '" + image_path + "'").read().strip()
    libmagic_output = libmagic_output.split(":", 1)[1]
    if "PNG" in libmagic_output:
        return "png"
    if "JPEG" in libmagic_output:
        return "jpg"
    if "GIF" in libmagic_output:
        return "gif"
    if "PC bitmap" in libmagic_output:
        return "bmp"
    return None



def get_image_size(imagepath:str):
    image = Image.open(imagepath)
    return image.size

@lru_cache(maxsize=1)
def get_mongo_collection() -> Collection:
    config = get_config()
    mongo_client = pymongo.MongoClient("mongodb://{}:{}/".format(config['mongodb-host'], config['mongodb-port']))
    mongo_collection = mongo_client[config['mongodb-database']][config['mongodb-collection']]
    return mongo_collection

def calc_md5(filepath):
    with open(filepath, 'rb') as f:
        md5 = hashlib.md5()
        while True:
            data = f.read(4096)
            if not data:
                break
            md5.update(data)
        return md5.hexdigest()

def get_full_path(basedir, basename):
    md5hash, ext = basename.split(".") 
    folder_path = "{}/{}/{}/".format(basedir, ext, md5hash[:2])
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    return "{}{}".format(folder_path, basename)

if __name__ == "__main__":
    print(calc_md5("../image_dataset/000001x2.png"))