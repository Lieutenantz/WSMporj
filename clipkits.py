import torch
import clip
def TextToFeature(text):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    texts = clip.tokenize([text]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(texts)
    return text_features[0]

def ImageToFeature(image):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    with torch.no_grad():
        feature = model.encode_image(preprocess(image).unsqueeze(0).to(device)).squeeze(0)
    return feature
