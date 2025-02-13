FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

# 设置环境变量以避免 tzdata 交互式配置
ENV DEBIAN_FRONTEND=noninteractive
ENV TIMEZONE=Asia/Shanghai

# 更新 apt 源
RUN apt-get update

# 安装 tzdata 并配置时区
RUN apt-get install -y tzdata \
    && ln -fs /usr/share/zoneinfo/$TIMEZONE /etc/localtime \
    && dpkg-reconfigure -f noninteractive tzdata

# 安装 git 和其他依赖
RUN apt-get install -y git ffmpeg libsm6 libxext6 libgl1

# 安装其他基础库
RUN apt-get install -y \
        wget build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev \
        libreadline-dev libffi-dev libsqlite3-dev libbz2-dev liblzma-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 使用 pip 安装 PyTorch 和其他库
RUN --mount=type=cache,target=/root/.cache/pip \
    git+https://github.com/TencentARC/GFPGAN.git@8d2447a2d918f8eba5a4a01463fd48e45126a379 \
    git+https://github.com/openai/CLIP.git@d50d76daa670286dd6cacf3bcd80b5e4823fc8e1 \
    git+https://github.com/mlfoundations/open_clip.git@v2.20.0

# 准备 tcmalloc
RUN apt-get -y install libgoogle-perftools-dev && apt-get clean
ENV LD_PRELOAD=libtcmalloc.so

# 创建环境目录并安装其他依赖
RUN mkdir -p /env
COPY ./env/* /env
RUN cd /env && \
    pip install -r requirements_wy.txt -i https://mirrors.aliyun.com/pypi/simple
