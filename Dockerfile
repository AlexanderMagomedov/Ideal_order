FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip && \
    pip install -r /app/requirements.txt

EXPOSE 8000