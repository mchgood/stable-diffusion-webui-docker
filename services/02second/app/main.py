# define the app
import asyncio
import os
import sys
import threading

# 获取根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 将根目录添加到path中
sys.path.append(BASE_DIR)
from embedding.log import log
from starlette.middleware.base import BaseHTTPMiddleware

from embedding.mq.receive import Text2vecConsumer, VitLargeConsumer
from embedding.text_image_embedding import DamoClipLargeInstance
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from embedding.entity.text_request import TextItems, MultiItems, MultiTypeList, ItemType
from embedding.image_embedding import ClipCnVitB16Instance
from embedding.text_embedding import MODEL_DICT


class RequestLoggerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        log.info(f"Received request: {request.method} {request.url}")
        response = await call_next(request)
        log.info(f"Sent response: {response.status_code}")
        return response


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])
app.add_middleware(RequestLoggerMiddleware)


@app.get('/ai-model-server')
async def index():
    return {"message": "hello world"}


@app.post('/ai-model-server/text2vec')
async def text2vec(item: TextItems):
    try:
        instance = MODEL_DICT.get(item.model)

        if instance is None:
            return {'status': False, 'msg': f"Model {item.model} not found supported models: {MODEL_DICT.keys()}"}, 400
        # 使用 asyncio.to_thread 将同步方法放入线程中执行
        result = await asyncio.to_thread(instance.embedding, item.input)
        log.debug(f"Successfully get sentence embeddings")
        return result
    except Exception as e:
        log.error(e)
        return {'status': False, 'msg': e}, 400


@app.post('/ai-model-server/multi-modal/vitb16/no-type')
async def vitb16NoType(items: MultiTypeList):
    try:
        result_embeddings = []
        list_types = items.split_by_type()
        for list_type in list_types:
            if list_type.get("type") == ItemType.text:
                results = ClipCnVitB16Instance.text_embedding(list_type.get("items"))
                result_embeddings.extend(results)
            elif list_type.get("type") == ItemType.image:
                results = ClipCnVitB16Instance.image_embedding(list_type.get("items"))
                result_embeddings.extend(results)
        log.debug(f"Successfully get sentence embeddings")
        return result_embeddings
    except Exception as e:
        log.error(e)
        return {'status': False, 'msg': e}, 400


@app.post('/ai-model-server/multi-modal/vitb16/with-type')
async def vitb16WithType(items: MultiItems):
    try:
        result_embeddings = []
        if items.type == ItemType.text:
            result_embeddings = ClipCnVitB16Instance.text_embedding(items.input)
        elif items.type == ItemType.image:
            result_embeddings = ClipCnVitB16Instance.image_embedding(items.input)
        log.debug(f"Successfully get sentence embeddings")
        return result_embeddings
    except Exception as e:
        log.error(e)
        return {'status': False, 'msg': e}, 400


@app.post('/ai-model-server/multi-modal/vitl/no-type')
async def vitlNoType(items: MultiTypeList):
    try:
        result_embeddings = []
        list_types = items.split_by_type()
        for list_type in list_types:
            if list_type.get("type") == ItemType.text:
                results = DamoClipLargeInstance.text_embedding(list_type.get("items"))
                result_embeddings.extend(results)
            elif list_type.get("type") == ItemType.image:
                results = DamoClipLargeInstance.image_embedding(list_type.get("items"))
                result_embeddings.extend(results)
        log.debug(f"Successfully get sentence embeddings")
        return result_embeddings
    except Exception as e:
        log.error(e)
        return {'status': False, 'msg': e}, 400


@app.post('/ai-model-server/multi-modal/vitl/with-type')
async def vitlWithType(items: MultiItems):
    try:
        result_embeddings = []
        if items.type == ItemType.text:
            result_embeddings = DamoClipLargeInstance.text_embedding(items.input)
        elif items.type == ItemType.image:
            result_embeddings = DamoClipLargeInstance.image_embedding(items.input)
        log.debug(f"Successfully get sentence embeddings")
        return result_embeddings
    except Exception as e:
        log.error(e)
        return {'status': False, 'msg': e}, 400

#
# def listen_text2vec():
#     queue_listen = Text2vecConsumer(exchange="vector_direct", routing_key="vector_direct_text2vec", queue="text2vec")
#     queue_listen.run()
#
#
# def listen_vit_large():
#     queue_listen = VitLargeConsumer(exchange="vector_direct", routing_key="vector_direct_vit_large", queue="vit_large")
#     queue_listen.run()


if __name__ == '__main__':
    # log.info("starting mq")
    # consume_enable = os.getenv("consume.enable", "true") == "true"
    # if consume_enable:
    #     threading.Thread(target=listen_text2vec).start()
    #     threading.Thread(target=listen_vit_large).start()
    #     log.info("started mq")
    log.info("starting web")
    uvicorn.run(app=app, host='0.0.0.0', port=9090)
    log.info("started")
