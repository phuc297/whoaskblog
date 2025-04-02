# syntax=docker/dockerfile:1
ARG PYTHON_VERSION=3.12.3

#
# Stage 1
#

FROM node:21 AS node-build

RUN mkdir -p /app
WORKDIR /app

RUN apt update && apt install curl -y

RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.2/install.sh | bash

ENV NVM_DIR=/root/.nvm

RUN bash -c "source $NVM_DIR/nvm.sh && nvm install $NODE_VERSION"

ENTRYPOINT ["bash", "-c", "source $NVM_DIR/nvm.sh && exec \"$@\"", "--"]

CMD ["/bin/bash"]

COPY package*.json ./
RUN npm install
RUN npm install tailwindcss @tailwindcss/cli --save-dev
COPY . .

# RUN npx @tailwindcss/cli -i ./staticfiles/src/input.css -o ./staticfiles/src/output.css --watch

#
# Stage 2
#

FROM python:${PYTHON_VERSION}-slim as base

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY --from=node-build /app .

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,source=requirements.txt,target=requirements.txt \
    python -m pip install -r ./requirements.txt

COPY . .
