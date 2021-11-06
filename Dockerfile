FROM python:3.9.7-buster

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./ /app/
WORKDIR /app

