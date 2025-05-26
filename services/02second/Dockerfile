FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

# 设置使得在安装 Debian 软件包时不需要用户交互，常用于 Dockerfile 中以避免在构建过程中卡住
ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1
ENV ROOT=/app

COPY ./requirements.txt ./requirements.txt

RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
