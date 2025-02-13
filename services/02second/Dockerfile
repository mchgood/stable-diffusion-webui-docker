FROM pytorch/pytorch:1.13.1-cuda11.6-cudnn8-runtime

# 设置环境变量以避免 tzdata 交互式配置
ENV DEBIAN_FRONTEND=noninteractive
ENV TIMEZONE=Asia/Shanghai

# 更新 apt 源并安装必要的工具和库
RUN apt-get update && \
    apt-get install -y git ffmpeg libsm6 libxext6 libgl1 \
    wget build-essential zlib1g-dev libncurses5-dev libgdbm-dev \
    libnss3-dev libssl-dev libreadline-dev libffi-dev libsqlite3-dev \
    libbz2-dev liblzma-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 确保 pip 安装并升级
RUN python3 -m ensurepip && python3 -m pip install --upgrade pip

# 使用 pip 安装 GitHub 上的库
RUN pip install \
    git+https://github.com/TencentARC/GFPGAN.git@8d2447a2d918f8eba5a4a01463fd48e45126a379 \
    git+https://github.com/openai/CLIP.git@d50d76daa670286dd6cacf3bcd80b5e4823fc8e1 \
    git+https://github.com/mlfoundations/open_clip.git@v2.20.0

# 准备 tcmalloc
RUN apt-get -y install libgoogle-perftools-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# 创建环境目录并安装其他依赖
RUN mkdir -p /env
COPY ./env/requirements_wy.txt /env/
RUN pip install -r /env/requirements_wy.txt -i https://mirrors.aliyun.com/pypi/simple
