FROM nvcr.io/nvidia/tensorrt:24.08-py3

# 设置使得在安装 Debian 软件包时不需要用户交互，常用于 Dockerfile 中以避免在构建过程中卡住
ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1
ENV ROOT=/app

# 安装程序需要 curl（和证书）来下载发布归档
RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates vim

RUN pip install flagembedding>=1.3.4 fastapi>=0.115.12 loguru>=0.7.3 uvicorn>=0.34.2

RUN pip install onnxruntime-gpu==1.18.1 --extra-index-url https://aiinfra.pkgs.visualstudio.com/PublicPackages/_packaging/onnxruntime-cuda-12/pypi/simple/

# 下载最新的安装程序
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# 运行安装程序，然后将其删除
RUN sh /uv-installer.sh && rm /uv-installer.sh && mkdir /app

# 确保安装的二进制文件在 PATH 中
ENV PATH="/root/.cargo/bin/:$PATH"

ADD ./app /app

WORKDIR /app

RUN $HOME/.local/bin/uv sync
