FROM python:latest

WORKDIR /code
COPY ./requirements.txt /code/requirements.txt

RUN apt update -y

COPY ./app /code/app

EXPOSE 8000

RUN pip install -r requirements.txt