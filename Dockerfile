FROM python:3.8.2-alpine3.11
WORKDIR /app
COPY requirements.txt .
RUN apk add -U --no-cache alpine-sdk redis && \
  pip install --no-cache-dir -r requirements.txt
