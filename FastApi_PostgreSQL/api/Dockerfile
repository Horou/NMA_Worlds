FROM python:bullseye
LABEL authors="Horou"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /src

COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
COPY api /src/api

ENTRYPOINT uvicorn api.main:app --host 0.0.0.0 --port ${API_PORT} --proxy-headers --reload