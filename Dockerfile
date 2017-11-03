FROM jfloff/alpine-python:latest

MAINTAINER Pavel Krayzel "pkrayzel@gmail.com"

COPY . /app

RUN pip install -r /app/requirements.txt

EXPOSE 5000

CMD ["python", "/app/src/app.py"]
