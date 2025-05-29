from typing import List

from modelscope.pipelines import pipeline
from modelscope.preprocessors.image import load_image
from modelscope.utils.constant import Tasks
from pydantic import constr


class DamoClipLarge:
    device: str = "cpu"
    pipeline: pipeline
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DamoClipLarge, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.pipeline = pipeline(task=Tasks.multi_modal_embedding,
                                 model='/llm/base-model/vector-models/multi-modal_clip-vit-large-patch14_zh',
                                 model_revision='v1.0.1', device=self.device)

    def text_embedding(self, texts: List[constr]):
        text_embedding = self.pipeline.forward({'text': texts})['text_embedding']
        return text_embedding.detach().cpu().numpy().tolist()

    def image_embedding(self, urls: List[str]):
        image_list = [load_image(url) for url in urls]
        img_embedding = self.pipeline.forward({'img': image_list})['img_embedding']
        return img_embedding.detach().cpu().numpy().tolist()


DamoClipLargeInstance = DamoClipLarge()

if __name__ == '__main__':
    print(2222)
    print(DamoClipLargeInstance.text_embedding(["你好"]))
