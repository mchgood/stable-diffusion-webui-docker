FROM gaibu/sd-second:1.0.0

# 设置使得在安装 Debian 软件包时不需要用户交互，常用于 Dockerfile 中以避免在构建过程中卡住
ENV DEBIAN_FRONTEND=noninteractive PIP_PREFER_BINARY=1
ENV ROOT=/stable-diffusion-webui

# 拷贝代码
RUN mkdir -p ${ROOT} && mkdir -p /docker
COPY ./repository/${ROOT}/ ${ROOT}
COPY ./deploy/* /docker

RUN --mount=type=cache,target=/root/.cache/pip \
    cd ${ROOT} && \
    pip install -r requirements_versions.txt -i https://mirrors.aliyun.com/pypi/simple && \
    pip install --upgrade typing-extensions -i https://mirrors.aliyun.com/pypi/simple && \
    sed -i 's/in_app_dir = .*/in_app_dir = True/g' /opt/conda/lib/python3.10/site-packages/gradio/routes.py

WORKDIR ${ROOT}
ENV NVIDIA_VISIBLE_DEVICES=all
ENV CLI_ARGS=""
EXPOSE 7860
ENTRYPOINT ["/docker/entrypoint.sh"]
CMD python -u webui.py --listen --port 7860 ${CLI_ARGS}
