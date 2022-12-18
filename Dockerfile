FROM python:3.10-slim

ENV PIP_ROOT_USER_ACTION=ignore

WORKDIR /app

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .
