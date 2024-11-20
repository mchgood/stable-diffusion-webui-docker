FROM bash:alpine3.19

RUN apk update && apk add parallel aria2
COPY . /docker
RUN chmod +x /docker/download.sh
RUN /bin/sh /docker/download.sh
COPY ../../data/* /data
ENTRYPOINT ["/docker/download.sh"]
