FROM ubuntu:18.04

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

RUN apt update -y && \
    apt install -y python3 python3-dev python3-pip libssl-dev libffi-dev

COPY ./ ./opt/answers-service-repo
WORKDIR /opt/answers-service-repo

EXPOSE 5050

RUN make install-requirements

ENTRYPOINT ["python3"]
CMD ["setup.py"]
