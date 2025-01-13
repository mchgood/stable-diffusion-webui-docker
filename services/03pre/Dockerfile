FROM gaibu/sd-second:1.0.0

# 设置使得在安装 Debian 软件包时不需要用户交互，常用于 Dockerfile 中以避免在构建过程中卡住
ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1
ENV ROOT=/stable-diffusion-webui

# 拷贝代码
COPY ./deploy/* /docker

WORKDIR ${ROOT}
ENV NVIDIA_VISIBLE_DEVICES=all
ENV CLI_ARGS=""
EXPOSE 7860
ENTRYPOINT ["/docker/entrypoint.sh"]
CMD python -u webui.py --listen --port 7860 ${CLI_ARGS}
