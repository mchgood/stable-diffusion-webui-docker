import json
from enum import Enum
from typing import List, Any

from pydantic import BaseModel, constr, field_validator


class TextItems(BaseModel):
    input: List[constr(max_length=512)]
    model: str = "text2vec-base-chinese"

    def __getitem__(self, item):
        """
        兼容dict的用法
        :param item:
        :return:
        """
        return self.model_dump()[item]

    def get(self, key, default=None):
        """
        兼容dict的用法
        :param key:
        :return:
        """
        return getattr(self, key, default)

    @field_validator('input')
    @classmethod
    def check_input_length(cls, v: Any):
        for item in v:
            if len(item) > 512:
                raise ValueError('Length of input strings must be less than or equal to 512')
        return v


class ItemType(str, Enum):
    image = "image"
    text = "text"

    def __getitem__(self, item):
        """
        兼容dict的用法
        :param item:
        :return:
        """
        return self.model_dump()[item]

    def get(self, key, default=None):
        """
        兼容dict的用法
        :param key:
        :return:
        """
        return getattr(self, key, default)


class MultiItem(BaseModel):
    type: ItemType
    content: constr(max_length=512)

    def __getitem__(self, item):
        """
        兼容dict的用法
        :param item:
        :return:
        """
        return self.model_dump()[item]

    def get(self, key, default=None):
        """
        兼容dict的用法
        :param key:
        :return:
        """
        return getattr(self, key, default)


class MultiItems(BaseModel):
    type: ItemType
    input: List[str]

    @field_validator('input')
    @classmethod
    def check_input_length(cls, v: List[str]):
        for item in v:
            if len(item) > 512:
                raise ValueError('Length of input strings must be less than or equal to 512')
        return v

    def __getitem__(self, item):
        """
        兼容dict的用法
        :param item:
        :return:
        """
        return self.model_dump()[item]

    def get(self, key, default=None):
        """
        兼容dict的用法
        :param key:
        :return:
        """
        return getattr(self, key, default)


class MultiTypeList(BaseModel):
    input: List[MultiItem]

    def __getitem__(self, item):
        """
        兼容dict的用法
        :param item:
        :return:
        """
        return self.model_dump()[item]

    def get(self, key, default=None):
        """
        兼容dict的用法
        :param key:
        :return:
        """
        return getattr(self, key, default)

    def split_by_type(self):
        result = []
        current_list = []
        current_type = None
        for item in self.input:
            if item.type != current_type:
                if current_list:
                    result.append({"type": current_type, "items": current_list})
                current_list = [item.content]
                current_type = item.type
            else:
                current_list.append(item.content)
        result.append({"type": current_type, "items": current_list})
        return result


if __name__ == '__main__':
    # 测试
    input_data = MultiTypeList(input=[
        MultiItem(type=ItemType.image, content="a"),
        MultiItem(type=ItemType.image, content="b"),
        MultiItem(type=ItemType.text, content="c"),
        MultiItem(type=ItemType.text, content="d"),
        MultiItem(type=ItemType.image, content="e")
    ])

    result = input_data.split_by_type()
    print(json.dumps(result, ensure_ascii=False, default=lambda v: v.model_dump()))

    r = []
    a = [[1, 2], [2, 3]]
    c = [[4, 5], [6, 7]]
    r.extend(a)
    r.extend(c)
    print(r)
