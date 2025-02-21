#FROM python:3.9

#ADD . /src

#WORKDIR /src

FROM mysql:latest


RUN apt-get update && apt-get install -y python3 python3-pip && \
    pip3 install --no-cache-dir mysql-connector-python


ENV MYSQL_ROOT_PASSWORD=${{ secrets.MYSQL_ROOT_PASSWORD }}
ENV MYSQL_DATABASE=bi
ENV MYSQL_USER={{ secrets.MYSQL_USER }}
ENV MYSQL_PASSWORD=${{ secrets.MYSQL_PASSWORD }}

ADD . /src

WORKDIR /src

CMD ["bash", "-c", "service mysql start"]
