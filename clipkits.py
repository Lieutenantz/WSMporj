import torch
import clip
from PIL import Image
# def TextToFeature(text):
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     model, preprocess = clip.load("ViT-B/32", device=device)
#     texts = clip.tokenize([text]).to(device)
#     with torch.no_grad():
#         text_features = model.encode_text(texts)
#     return text_features[0]

# def ImageToFeature(image):
#     device = "cuda" if torch.cuda.is_available() else "cpu"
#     model, preprocess = clip.load("ViT-B/32", device=device)
#     with torch.no_grad():
#         feature = model.encode_image(preprocess(image).unsqueeze(0).to(device)).squeeze(0)
#     return feature
class ClipTool():
    def __init__(self):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        model, preprocess = clip.load("models/ViT-B-32.pt", device=device)
        self.device=device
        self.model=model
        self.preprocess=preprocess

    def TextToFeature(self,text):
        model=self.model
        device=self.device
        texts = clip.tokenize([text]).to(device)
        with torch.no_grad():
            text_features = model.encode_text(texts)
        return text_features[0]

    def ImageToFeature(self, image_path:str):
        """ 输入图片路径, 输出图片的feature向量"""
        image = Image.open(image_path)
        model = self.model
        device = self.device
        preprocess=self.preprocess
        with torch.no_grad():
            feature = model.encode_image(preprocess(image).unsqueeze(0).to(device)).squeeze(0)
        return feature
    

