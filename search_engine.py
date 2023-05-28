import numpy as np
from utils import get_config, get_mongo_collection
import torch
import clip

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
        self.featrue_dim = config['model_dim']
        self.mongo_collection = get_mongo_collection()
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model, _ = clip.load("ViT-B/32", device=self.device)
        
    
    def _get_search_filter(self, args):
        '''
        在长宽上限制图片大小，转为数据库搜索格式
        return ret: dict()
        '''
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

    def _search(self, query_feature, topn, size_condition={}):
        '''
        search function
        '''
        cursor = self.mongo_collection.find(self._get_search_filter(size_condition)) # 获取限制图片大小的数据
        feature_list = []
        index_list = []
        for item in cursor:
            feature_list.append(np.frombuffer(item['featrue'], dtype=float32))
            index_list.append(item['filename'])
        
        if len(feature_list) > 0:
            feature_list = np.array(feature_list)
            cosine_sim_score_list = cosine_similarity(query_feature, feature_list)
        else:
            return [], []
        
        top_n_idx = np.argsort(cosine_sim_score_list)[::-1][:topn]
        top_n_index = [index_list[idx] for idx in top_n_idx]
        top_n_score = [float(cosine_sim_score_list[idx]) for idx in top_n_idx]

        return top_n_filename, top_n_score
    
    def serve(self, query, topn=20, minimum_width=None, maximum_width=None, minimum_height=None, maximum_height=None):
        '''
        Searching according to query text
        Args:
            query (`str`): text for searching
            topn (`int`): number of expected pictures to return
            minimum_width(`int`, *Optional*): minimum figure width
            maximum_width(`int`, *Optional*): maximum figure width
            minimum_height(`int`, *Optional*): minimum figure height
            maximum_height(`int`, *Optional*): maximum figure height
        return:
            topn_index(`List[str]`): indices in DB or paths of the result figure
            topn_score(`List[float]`): scores of the result figure
        '''
        if isinstance(query, str):
            texts = clip.tokenize([query]).to(self.device)
            with torch.no_grad():
                text_features = self.model.encode_text(texts)
            text_feature = text_features[0]
            print(text_feature.size())
        else:
            assert False, "Invalid query (input) type"
        
        args = {}
        if minimum_width != None: args['minimum_width'] = minimum_width
        if maximum_width != None: args['maximum_width'] = maximum_width
        if minimum_height != None: args['minimum_height'] = minimum_height
        if maximum_height != None: args['minimum_height'] = maximum_height
        
        topn_index, topn_score = self._search(text_feature, topn, args)
        return topn_index, topn_score



if __name__ == "__main__":
    config = get_config()
    SE = SearchEngine(config)
    
    query = "一辆白色汽车"

    indices, scores = SE.serve(query, topn=10, minimum_width=200, maximum_width=1000, minimum_height=400, maximum_height=800)