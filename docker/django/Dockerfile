FROM python:3.9.6-slim-buster

ENV  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
    build-essential \
    python3-dev \
    curl \
    make \
    gettext \
    git \
    libpq-dev \
    wget \
  # Cleaning cache:
  && apt-get autoremove -y && apt-get clean -y && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/requirements.txt
RUN  pip install --no-cache-dir -r /app/requirements.txt
COPY ../.. /app
WORKDIR /app

