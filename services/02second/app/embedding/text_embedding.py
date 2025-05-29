from abc import abstractmethod, ABC
from typing import List
import os
from pydantic import constr
import torch
from sentence_transformers import SentenceTransformer

CPU_DEVICE = "cpu"
GPU_DEVICE = "cuda:0"
# 如果使用
if torch.cuda.is_available() and torch.cuda.device_count() > 1 and "cuda" in GPU_DEVICE:
    GPU_DEVICE = 'cuda:1'

TEXT2VEC_LARGE_CHINESE_MODEL_PATH = os.environ.get("TEXT2VEC_LARGE_CHINESE_MODEL_PATH",
                                                   "/llm/base-model/text2vec-large-chinese/V20250523112239645/")
TEXT2VEC_BASE_CHINESE_MODEL_PATH = os.environ.get("TEXT2VEC_BASE_CHINESE_MODEL_PATH",
                                                  "/llm/base-model/text2vec-base-chinese/V20250526173905680/")
TEXT2VEC_BASE_CHINESE_INT8_MODEL_PATH = os.environ.get("TEXT2VEC_BASE_CHINESE_INT8_MODEL_PATH",
                                                       "/llm/base-model/text2vec-base-chinese/V20250526173905680/text2vec-base-chinese/")
BGE_M3_MODEL_PATH = os.environ.get("BGE_M3_MODEL_PATH", "/llm/base-model/bge-m3/V20250528162958325/")


class BaseEmbedding(ABC):
    @abstractmethod
    def embedding(self, text: List[constr]):
        pass

    @abstractmethod
    def type(self) -> str:
        pass


class Text2vectBaseChinese(BaseEmbedding):
    model: SentenceTransformer

    def __init__(self):
        self.model = SentenceTransformer(
            model_name_or_path=TEXT2VEC_BASE_CHINESE_MODEL_PATH,
            local_files_only=True,
            device=GPU_DEVICE,
            backend="torch",
            model_kwargs={"file_name": "pytorch_model.bin"},
        )

    def embedding(self, text: List[constr]):
        embeddings = self.model.encode(text, normalize_embeddings=True)
        return embeddings.tolist()

    def type(self) -> str:
        return 'text2vec-base-chinese'


class Text2vectBaseChineseInt8(BaseEmbedding):
    model: SentenceTransformer

    def __init__(self):
        self.model = SentenceTransformer(
            model_name_or_path=TEXT2VEC_BASE_CHINESE_INT8_MODEL_PATH,
            local_files_only=True,
            device=CPU_DEVICE,
            backend="onnx",
            model_kwargs={"file_name": "model_qint8_avx512_vnni.onnx"},
        )

    def embedding(self, text: List[constr]):
        embeddings = self.model.encode(text, normalize_embeddings=True)
        return embeddings.tolist()

    def type(self) -> str:
        return 'text2vec-base-chinese-int8'


class Text2vectLargeChinese(BaseEmbedding):
    model: SentenceTransformer

    def __init__(self):
        self.model = SentenceTransformer(
            model_name_or_path=TEXT2VEC_LARGE_CHINESE_MODEL_PATH,
            local_files_only=True,
            device=GPU_DEVICE,
            backend="torch",
            model_kwargs={"file_name": "pytorch_model.bin"},
        )

    def embedding(self, text: List[constr]):
        embeddings = self.model.encode(text, normalize_embeddings=True)
        return embeddings.tolist()

    def type(self) -> str:
        return 'text2vec-large-chinese'


class BgeM3(BaseEmbedding):
    model: SentenceTransformer

    def __init__(self):
        self.model = SentenceTransformer(
            model_name_or_path=BGE_M3_MODEL_PATH,
            local_files_only=True,
            device=GPU_DEVICE,
            backend="torch",
            model_kwargs={"file_name": "pytorch_model.bin"},
        )

    def embedding(self, text: List[constr]):
        embeddings = self.model.encode(text, normalize_embeddings=True)
        return embeddings.tolist()

    def type(self) -> str:
        return 'bge-m3'


Text2vectBaseChineseInstance = Text2vectBaseChinese()
Text2vectBaseChineseInt8Instance = Text2vectBaseChineseInt8()
Text2vectLargeChineseInstance = Text2vectLargeChinese()
BgeM3Instance = BgeM3()

MODEL_DICT = {
    Text2vectBaseChineseInstance.type(): Text2vectBaseChineseInstance,
    Text2vectBaseChineseInt8Instance.type(): Text2vectBaseChineseInt8Instance,
    Text2vectLargeChineseInstance.type(): Text2vectLargeChineseInstance,
    BgeM3Instance.type(): BgeM3Instance,
}
