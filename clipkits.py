import torch
import clip
def TextToFeature(text):
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model, preprocess = clip.load("ViT-B/32", device=device)
    texts = clip.tokenize([text]).to(device)
    with torch.no_grad():
        text_features = model.encode_text(texts)
    return text_features[0]