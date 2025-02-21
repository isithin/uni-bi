#FROM python:3.9

#ADD . /src

#WORKDIR /src

FROM mysql:latest


RUN apt-get update && apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir mysql-connector-python

ADD . /src

WORKDIR /src

CMD ["bash", "-c", "service mysql start"]
