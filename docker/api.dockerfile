# syntax = docker/dockerfile:1.4

FROM python:latest AS builder

RUN mkdir /setup

WORKDIR /app

RUN poetry export -o .\\Docker\\requirements.txt --no-cache --without-hashes --without-urls

COPY requirements.txt /setup/

RUN --mount=type=cache,target=/root/.cache/pip pip install -r /setup/requirements.txt

COPY ../src ./
