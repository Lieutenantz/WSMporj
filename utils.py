#!/usr/bin/env python3
import os
import json
import hashlib
from functools import lru_cache
import pymongo
from pymongo.collection import Collection

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
    """keep function, implement straight"""
    return "png"