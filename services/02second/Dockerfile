FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime

# 设置使得在安装 Debian 软件包时不需要用户交互，常用于 Dockerfile 中以避免在构建过程中卡住
ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1

# 准备图像处理和一般开发环境
RUN --mount=type=cache,target=/var/cache/apt \
  apt-get update && \
  # we need those
  apt-get install -y fonts-dejavu-core rsync jq moreutils git \
  # extensions needs those
  ffmpeg libglfw3-dev libgles2-mesa-dev pkg-config libcairo2 libcairo2-dev build-essential

RUN --mount=type=cache,target=/root/.cache/pip \
  pip install pyngrok xformers==0.0.26.post1 -i https://mirrors.aliyun.com/pypi/simple \
  git+https://github.com/TencentARC/GFPGAN.git@8d2447a2d918f8eba5a4a01463fd48e45126a379 \
  git+https://github.com/openai/CLIP.git@d50d76daa670286dd6cacf3bcd80b5e4823fc8e1 \
  git+https://github.com/mlfoundations/open_clip.git@v2.20.0

# 准备 tcmalloc
RUN apt-get -y install libgoogle-perftools-dev && apt-get clean
ENV LD_PRELOAD=libtcmalloc.so
