#!/usr/bin/env python3
import os
import shutil
from glob import glob
from datetime import datetime
from PIL import Image

import pymongo
from pymongo.collection import Collection
import utils

try:
    import clip_model
except ModuleNotFoundError:
    print("No module named 'clip_model'")
    clip_tag = False
else:
    clip_tag = True

def import_single_image(filepath, feature_str:str, config:dict, mongo_collection, copy=False):
    filetype = utils.get_file_type(filepath)
    if filetype is None:
        print("skip file:", filepath)
        return

    image_size = Image.open(filepath).size()
    image_feature = utils.str_2_feature_numpy(feature_str)

    if copy:
        md5hash = utils.calc_md5(filename)
