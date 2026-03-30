FROM python:3.12-alpine

# Ставим zabbix_sender
RUN apk add --no-cache zabbix-utils bash

WORKDIR /app
COPY . .
RUN pip install flask

ENV ZABBIX_SERVER=10.0.0.10
ENV HOST_NAME=My_Virtual_Host

EXPOSE 5000
CMD ["python", "app.py"]
