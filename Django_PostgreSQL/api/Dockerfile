FROM python:bullseye
LABEL authors="Horou"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /src/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /src/requirements.txt
COPY api /src/api

WORKDIR /src/api

ENTRYPOINT ["scripts/run.sh"]