FROM library/python:alpine3.7

RUN pip install Flask==0.12.2

ADD ./src /opt/intervention-ninja
WORKDIR /opt/intervention-ninja

EXPOSE 80

CMD ["python", "app.py"]
