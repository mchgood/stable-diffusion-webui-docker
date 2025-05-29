import os
from typing import Optional, List, Union, Dict

from pymilvus import MilvusClient

from embedding.log import log


class MilvusOp:
    """
    阿里云dashvector操作对象

    """

    def __init__(self, endpoint: Optional[str] = None, username: Optional[str] = None, password: Optional[str] = None,
                 database: Optional[str] = "default"):
        """
        初始化函数
        :param endpoint: 服务地址,形如http://c-aa529ad391d07dd2.milvus.aliyuncs.com:19530
        :param username: 用户名
        :param password: 密码
        """
        log.info("{},{},{},{}", endpoint, username, password, database)
        # if not endpoint:
        #     endpoint = os.environ.get("MILVUS_ENDPOINT")
        #     if not endpoint:
        #         raise ValueError("缺失endpoint参数")
        # if not username:
        #     username = os.environ.get("MILVUS_USERNAME")
        # if not password:
        #     password = os.environ.get("MILVUS_PASSWORD")
        # if not username:
        #     client = MilvusClient(
        #         uri=endpoint,
        #         db_name=database
        #     )
        # else:
        #     client = MilvusClient(
        #         uri=endpoint,
        #         token=f"{username}:{password}",
        #         db_name=database
        #     )
        # self.__client = client

    def add_data(self, collection_name: str,
                 data: Union[Dict, List[Dict]],
                 timeout: Optional[float] = None,
                 partition_name: Optional[str] = "", **kwargs) -> List[any]:
        res = self.__client.insert(collection_name=collection_name, data=data, timeout=timeout,
                                   partition_name=partition_name,
                                   **kwargs)
        return res.get("ids")

    def query(self, collection_name: str,
              filter: str = "",
              output_fields: Optional[List[str]] = None,
              timeout: Optional[float] = None,
              ids: Optional[Union[List, str, int]] = None,
              partition_names: Optional[List[str]] = None, **kwargs) -> List[dict]:
        return self.__client.query(collection_name=collection_name, filter=filter, output_fields=output_fields,
                                   timeout=timeout,
                                   ids=ids, partition_names=partition_names, **kwargs)

    def search_multiple(self, collection_name: str,
                        data: Union[List[List], List],
                        filter: str = "",
                        limit: int = 10,
                        output_fields: Optional[List[str]] = None,
                        search_params: Optional[dict] = None,
                        timeout: Optional[float] = None,
                        partition_names: Optional[List[str]] = None,
                        anns_field: Optional[str] = None, **kwargs) -> List[List[dict]]:
        return self.__client.search(collection_name=collection_name, data=data, filter=filter, limit=limit,
                                    output_fields=output_fields, search_params=search_params, timeout=timeout,
                                    partition_names=partition_names, anns_field=anns_field, **kwargs)

    def search(self, collection_name: str,
               data: list,
               filter: str = "",
               limit: int = 10,
               output_fields: Optional[List[str]] = None,
               search_params: Optional[dict] = None,
               timeout: Optional[float] = None,
               partition_names: Optional[List[str]] = None,
               anns_field: Optional[str] = None, **kwargs) -> List[dict]:
        result = self.__client.search(collection_name=collection_name, data=[data], filter=filter, limit=limit,
                                      output_fields=output_fields,
                                      search_params=search_params, timeout=timeout, partition_names=partition_names,
                                      anns_field=anns_field, **kwargs)
        return result[0]

    def update(self,
               collection_name: str,
               data: Union[Dict, List[Dict]],
               timeout: Optional[float] = None,
               partition_name: Optional[str] = "",
               **kwargs):
        desc = self.__client.describe_collection(collection_name=collection_name)
        if desc.get("auto_id"):
            if isinstance(data, Dict):
                data = [data]
            id_list = [d.pop("id") for d in data]
            self.delete(collection_name=collection_name, ids=id_list, timeout=timeout, partition_name=partition_name,
                        **kwargs)
            return self.add_data(collection_name=collection_name, data=data, timeout=timeout,
                                 partition_name=partition_name, **kwargs)
        else:
            self.__client.upsert(collection_name=collection_name, data=data, timeout=timeout,
                                 partition_name=partition_name, **kwargs)
            return [d["id"] for d in data]

    def delete(self, collection_name: str,
               ids: Optional[Union[List, str, int]] = None,
               timeout: Optional[float] = None,
               filter: Optional[str] = "",
               partition_name: Optional[str] = "",
               **kwargs) -> int:
        result = self.__client.delete(collection_name=collection_name, ids=ids, timeout=timeout, filter=filter,
                                      partition_name=partition_name, **kwargs)
        return result.get("delete_count", 0)

    @classmethod
    def split_list(cls, lst: List[any], size: int = 200) -> List[List[any]]:
        """
        将列表lst切分为每个子列表包含size个元素
        """
        return [lst[i:i + size] for i in range(0, len(lst), size)]
