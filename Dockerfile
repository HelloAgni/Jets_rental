FROM python:3.10-slim

WORKDIR /proj

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY dev-requirements.txt ./

RUN pip3 install -r dev-requirements.txt --no-cache-dir

COPY app/ app/
COPY alembic/ alembic/
COPY alembic.ini ./