import numpy as np
from utils import read_config, get_mongo_collection

def cosine_similarity(query_feature, feature_list):
    '''
    对query的文本feature与图片列表的feature计算余弦相似度
    query_feature: list: (dim)
    feature_list:  list: (image_num, dim)
    return: list: (image_num)
    '''
    query_feature = query_feature / np.linalg.norm(query_feature, keepdims=True) # 归一化query feature
    feature_list = feature_list / np.linalg.norm(feature_list, axis=1, keepdims=True) # 归一化image feature
    score = query_feature.dot(feature_list.T)
    return score


class SearchEngine:
    def __init__(self, config):
        self.config = config
        self.featrue_dim = config['model_dim'] #TODO
        self.mongo_collection = get_mongo_collection()
    
    def _get_search_filter(self, args):
        # 先在长宽上限制图片大小
        ret = {}
        if len(args) == 0: return ret
        if 'minimum_width' in args:
            if 'width' not in ret: ret['width'] = {}
            ret['width']['$gte'] = int(args['minimum_width'])
        if 'maximum_width' in args:
            if 'width' not in ret: ret['width'] = {}
            ret['width']['$lte'] = int(args['maximum_width'])
        if 'minimum_height' in args:
            if 'height' not in ret: ret['height'] = {}
            ret['height']['$gte'] = int(args['minimum_height'])
        if 'maximum_height' in args:
            if 'height' not in ret: ret['height'] = {}
            ret['height']['$lte'] = int(args['maximum_height'])
        return ret

    def search(self, query_feature, topn=20, size_condition={}):
        '''
        根据query_feature搜索数据库
        topn: 搜索结果取最相似的 topn 个
        size_condition: 图片尺寸限制
            {
                'minimum_width': ...,
                'maximum_width': ...,
                'minimum_height': ...,
                'maximum_height': ...
            }
        return: topn_filename: list(topn) # 最相似的 topn 个图片路径/索引
                topn_score: list(topn) # 最相似的 topn 个图片相似度分数
        '''
        cursor = self.mongo_collection.find(self._get_search_filter(size_condition)) # 获取限制图片大小的数据
        feature_list = []
        filename_list = []
        for item in cursor:
            feature_list.append(np.frombuffer(item['featrue'], dtype=float32))
            filename_list.append(item['filename'])
        
        if len(feature_list) > 0:
            feature_list = np.array(feature_list)
            cosine_sim_score_list = cosine_similarity(query_feature, feature_list)
        else:
            return [], []
        
        top_n_idx = np.argsort(cosine_sim_score_list)[::-1][:topn]
        top_n_filename = [filename_list[idx] for idx in top_n_idx]
        top_n_score = [float(cosine_sim_score_list[idx]) for idx in top_n_idx]

        return top_n_filename, top_n_score


if __name__ == "__main__":
    config = read_config()
    SE = SearchEngine(config)

    print(SE.search(query_feature, 10))