# WSMporj
## jcq
import_images.py 导入了clip_model库, 但是目前仓库没有clip_model库的实现

config.json只添加了导入数据库的必要配置数据, 并不是参考仓库中的完整config

使用md5命名的图片文件夹data并没有放在仓库中, 因为有3GB, 如果全部放进去, pull 和 push 很麻烦, 如果需要再说

## jcq 6.2
更新了 import_images.py
更新了mongoDB数据库,wsm.images添加了filename索引,即filename可以直接作为索引使用
```json
wsm> db.images.getIndexes()
[
  { v: 2, key: { _id: 1 }, name: '_id_' },
  { v: 2, key: { filename: 1 }, name: 'filename_1', unique: true }
]
```