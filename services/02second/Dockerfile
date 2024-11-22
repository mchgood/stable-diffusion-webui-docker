FROM pytorch/pytorch:2.3.0-cuda12.1-cudnn8-runtime

# 设置使得在安装 Debian 软件包时不需要用户交互，常用于 Dockerfile 中以避免在构建过程中卡住
ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1

# 准备图像处理和一般开发环境
RUN --mount=type=cache,target=/var/cache/apt \
  apt-get update && \
  # we need those
  apt-get install -y fonts-dejavu-core rsync jq moreutils \
  # extensions needs those
  ffmpeg libglfw3-dev libgles2-mesa-dev pkg-config libcairo2 libcairo2-dev build-essential

# 准备 tcmalloc
RUN apt-get -y install libgoogle-perftools-dev && apt-get clean
ENV LD_PRELOAD=libtcmalloc.so
