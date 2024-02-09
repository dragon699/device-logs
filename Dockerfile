FROM python:3.9-slim

WORKDIR /app

COPY ./src/* ./

RUN apt-get update && \
    apt-get -y install socat && \
    pip install --no-cache-dir -r requirements.txt
