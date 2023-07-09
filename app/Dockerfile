FROM pytorch/pytorch:2.0.1-cuda11.7-cudnn8-runtime

ARG DEBIAN_FRONTEND=noninteractive
WORKDIR /app

COPY requirements.txt $WORKDIR

RUN apt-get update && apt-get clean && apt-get install ffmpeg libsm6 libxext6 -y

RUN pip install -U pip && \
    pip install -r requirements.txt --no-cache-dir

COPY . $WORKDIR
