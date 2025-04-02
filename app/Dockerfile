# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.12

#
# Stage 1
#

# FROM node:21 AS node-build

# RUN mkdir -p /node_build
# WORKDIR /node_build

# COPY . .
# RUN npm install tailwindcss @tailwindcss/cli
# COPY . .

#
# Stage 2
#

FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r ./requirements.txt

COPY . .