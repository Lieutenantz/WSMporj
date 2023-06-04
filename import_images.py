#!/usr/bin/env python3
import os
import shutil
from glob import glob
from datetime import datetime
import numpy as np
import pymongo
from pymongo.collection import Collection

from tqdm import tqdm

import clipkits

import utils

def import_single_image(image_path: str, feature: np.ndarray,
                        config: dict, mongo_collection: Collection, copy=False, printlog=False):
    """
        一张新图片地址, 和由模型生成的feature存入指定的mongo_collection中
        copy: 是否复制到指定文件夹中
        printlog: 是否打印成功插入数据库的信息: <文件索引名> inserted successfully
    """
    image_type = utils.get_file_type(image_path)
    if image_type is None:
        print("skip file:", image_path)
        return

    image_size = utils.get_image_size(image_path)

    feature = feature.numpy().astype(config['storage-type']) # float32

    if copy:
        md5hash = utils.calc_md5(image_path)
        new_basename = md5hash + '.' + image_type # new name
        new_full_path = utils.get_full_path(config['import-image-base'], new_basename)

        if os.path.isfile(new_full_path):
            print("duplicate file:", image_path)
            return
        
        shutil.copy2(image_path, new_full_path)
        stat = os.stat(new_full_path)
    else:
        stat = os.stat(image_path)
        new_full_path = image_path

    image_mtime = datetime.fromtimestamp(stat.st_mtime)
    image_datestr = image_mtime.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

    # save to mongodb
    document = {
        'filename': new_full_path, # md5 name
        'extension': image_type,
        'height': image_size[1],
        'width': image_size[0],
        'filesize': stat.st_size,
        'date': image_datestr,
        'feature': feature.tobytes() # feature 存储的是byte格式
    }

    x = mongo_collection.insert_one(document)
    if printlog:
        print(f"{document['filename']} insert successfully")
    return x

def import_dir(base_dir: str, cliptool: clipkits.ClipTool,
               config: dict, mongo_collection: Collection, copy=False, printlog=False):
    """
        从一个存放着多张图片的文件夹中导入所有图片到数据库中
    """
    filelist = glob(os.path.join(base_dir, '**/*'), recursive=True) # base_dir下的所有文件和文件夹列表
    filelist = [f for f in filelist if os.path.isfile(f)]

    for filename in tqdm(filelist):
        feature = cliptool.ImageToFeature(filename)
        import_single_image(filename, feature, config, mongo_collection, copy=copy, printlog=printlog)

def tools(path:str):
    config = utils.get_config()
    mongo_collection = utils.get_mongo_collection()
    cliptool = clipkits.ClipTool()
    if os.path.exists(path):
        if os.path.isfile(path):
            image_feature = cliptool.ImageToFeature(path)
            import_single_image(path, image_feature,config, mongo_collection, copy=True, printlog=False)
        elif os.path.isdir(path):
            import_dir(path, cliptool, config, mongo_collection, True,False)
        return True # 图片加载成功
    else:
        return False # 图片加载失败


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--copy', action='store_true')
    parser.add_argument('path', help="an image path or a directory path")
    parser.add_argument('--printlog', action='store_true', help="print insertion log")
    args = parser.parse_args()
    config = utils.get_config()
    mongo_collection = utils.get_mongo_collection()
    cliptool = clipkits.ClipTool()
    path = args.path
    if os.path.exists(path):
        if os.path.isfile(path):
            image_feature = cliptool.ImageToFeature(path)
            import_single_image(path, image_feature,config, mongo_collection, copy=args.copy, printlog=args.printlog)
        elif os.path.isdir(path):
            import_dir(args.path, cliptool, config, mongo_collection, args.copy,args.printlog)
    else:
        print("the path does not exist!!")

if __name__ == '__main__':
    main()