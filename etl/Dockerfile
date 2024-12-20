FROM python:3.12

WORKDIR /app

ENV PYTHONPATH=/app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

COPY kafka_to_clickhouse/ ./etl/kafka_to_clickhouse
