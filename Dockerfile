FROM library/python:alpine3.7

ADD ./src /opt/intervention-ninja
WORKDIR /opt/intervention-ninja

RUN pip install Flask==0.12.2

EXPOSE 80

CMD ["python", "app.py"]
