# -*- coding: utf-8 -*-
from typing import List

import cn_clip.clip as clip
import requests
from PIL import Image
from cn_clip.clip import load_from_name
from cn_clip.clip.model import CLIP
from pydantic import constr
from torchvision.transforms.v2 import Compose


class ClipCnVitB16:
    device: str = "cpu"
    model: CLIP
    preprocess: Compose
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ClipCnVitB16, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        model, preprocess = load_from_name("ViT-B-16", device=self.device,
                                           download_root='/llm/base-model/vector-models/clip_cn/')
        model.eval()
        self.model = model
        self.preprocess = preprocess

    def text_embedding(self, texts: List[constr]):
        text = clip.tokenize(texts).to(self.device)
        text_features = self.model.encode_text(text)
        return text_features.detach().numpy().tolist()

    def image_embedding(self, urls: List[str]):
        images = []
        for url in urls:
            img = Image.open(requests.get(url, stream=True).raw)
            image = self.preprocess(img).unsqueeze(0).to(self.device)
            image_feature = self.model.encode_image(image)
            images.append(image_feature.detach().numpy().tolist()[0])
        return images


ClipCnVitB16Instance = ClipCnVitB16()

if __name__ == '__main__':
    a = ClipCnVitB16Instance.text_embedding(
        ['https://one-peace-shanghai.oss-cn-shanghai.aliyuncs.com/modelscope_case/dog.JPEG',
         'https://one-peace-shanghai.oss-cn-shanghai.aliyuncs.com/modelscope_case/panda.JPEG'])

    print(a)
