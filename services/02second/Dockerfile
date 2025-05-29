ARG CUDA_VERSION=11.4.0
ARG CUDNN_VERSION=8
ARG OS_VERSION=18.04

# 从nvidia 官方镜像库拉取基础镜像
FROM nvidia/cuda:${CUDA_VERSION}-cudnn${CUDNN_VERSION}-devel-ubuntu${OS_VERSION}
LABEL maintainer="nietaiyang"

# ENV TRT_VERSION 7.2.3.4
# ENV TRT_VERSION 7.0.0.11
ENV TRT_VERSION 8.2.1.8
SHELL ["/bin/bash", "-c"]


# 将 apt 的升级源切换成 阿里云
RUN  sed -i s@/archive.ubuntu.com/@/mirrors.aliyun.com/@g /etc/apt/sources.list && \
            apt-get clean && \
            rm /etc/apt/sources.list.d/*

# 安装必要的库
RUN apt-get update && apt-get install -y software-properties-common
RUN add-apt-repository ppa:ubuntu-toolchain-r/test
RUN apt-get update && apt-get install -y --no-install-recommends \
    libcurl4-openssl-dev \
    wget \
    vim \
    zlib1g-dev \
    git \
    pkg-config \
    sudo \
    ssh \
    libssl-dev \
    pbzip2 \
    pv \
    bzip2 \
    unzip \
    devscripts \
    lintian \
    fakeroot \
    dh-make \
    build-essential \
    libgl1-mesa-glx


# 安装 python3 环境
RUN apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    python3-dev \
    python3-wheel &&\
    cd /usr/local/bin &&\
    ln -s /usr/bin/python3 python &&\
    ln -s /usr/bin/pip3 pip;

# 安装 TensorRT
RUN cd /tmp && sudo apt-get update

RUN version="8.2.1-1+cuda11.4" && \
    sudo apt-get install libnvinfer8=${version} libnvonnxparsers8=${version} libnvparsers8=${version} libnvinfer-plugin8=${version} libnvinfer-dev=${version} libnvonnxparsers-dev=${version} libnvparsers-dev=${version} libnvinfer-plugin-dev=${version} python3-libnvinfer=${version} &&\
    sudo apt-mark hold libnvinfer8 libnvonnxparsers8 libnvparsers8 libnvinfer-plugin8 libnvinfer-dev libnvonnxparsers-dev libnvparsers-dev libnvinfer-plugin-dev python3-libnvinfer

# 升级 pip 并切换成国内豆瓣源
RUN python3 -m pip install -i https://pypi.douban.com/simple/ --upgrade pip
RUN pip3 config set global.index-url https://pypi.douban.com/simple/
RUN pip3 install setuptools>=41.0.0

# 升级 Cmake（可选）
RUN cd /tmp && \
    wget https://github.com/Kitware/CMake/releases/download/v3.14.4/cmake-3.14.4-Linux-x86_64.sh && \
    chmod +x cmake-3.14.4-Linux-x86_64.sh && \
    ./cmake-3.14.4-Linux-x86_64.sh --prefix=/usr/local --exclude-subdir --skip-license && \
    rm ./cmake-3.14.4-Linux-x86_64.sh

# 设置环境变量和工作路径
ENV TRT_LIBPATH /usr/lib/x86_64-linux-gnu
ENV TRT_OSSPATH /workspace/TensorRT
ENV LD_LIBRARY_PATH="${LD_LIBRARY_PATH}:${TRT_OSSPATH}/build/out:${TRT_LIBPATH}"

# 设置语言环境为中文，防止 print 中文报错
ENV LANG C.UTF-8

ENV ROOT=/app

# 安装程序需要 curl（和证书）来下载发布归档
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates vim

# 下载最新的安装程序
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# 运行安装程序，然后将其删除
RUN sh /uv-installer.sh && rm /uv-installer.sh && mkdir /app

# 确保安装的二进制文件在 PATH 中
ENV PATH="/root/.cargo/bin/:$PATH"

ADD ./app /app

WORKDIR /app

RUN $HOME/.local/bin/uv sync
