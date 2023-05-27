#!/usr/bin/env python3
import os
import json
import hashlib
from functools import lru_cache
import pymongo
from pymongo.collection import Collection
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
    """keep function, implement straight"""
    return "png"


def str_2_feature_numpy(feature_str:str) -> np.ndarray:
    feature_str = re.sub('\s+',',',feature_str)
    return np.array(eval(feature_str),dtype=np.float32)


def read_config():
    with open(config.json) as f:
        con = json.load(f)
    return con


@lru_cache(maxsize=1)
def get_mongo_collection():
    config = read_config()
    mongo_client = pymongo.MongoClient("mongodb://{}:{}/".format(config['mongodb-host'], config['mongodb-port']))
    mongo_collection = mongo_client[config['mongodb-database']][config['mongodb-collection']]
    return mongo_collection