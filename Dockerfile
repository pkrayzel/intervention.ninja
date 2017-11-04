FROM jfloff/alpine-python:latest

MAINTAINER Pavel Krayzel "pkrayzel@gmail.com"

COPY . /app
WORKDIR /app/src

RUN pip install -r /app/requirements.txt

EXPOSE 5000

CMD ["python", "app.py"]
