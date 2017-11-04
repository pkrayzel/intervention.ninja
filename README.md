# intervention.ninja

The purpose of this project is to help people deal with difficult announcements to their friends / coworkers.

It uses flask micro-framework. 

## Running it in docker

``` 
docker build -t pkrayzel/intervention-ninja .
docker run -p 5000:5000 -d --env MAIL_USERNAME=username --env MAIL_PASSWORD=password -t pkrayzel/intervention-ninja  
```

## Running it locally outside docker

#### Create virtual environment
```
virtualenv ~/int -p python3
``` 

#### Activate it
```
source ~/int/bin/activate
```

#### Install all dependencies
```
pip install -r requirements.txt
```

#### Configure gmail smtp server

``` 
export MAIL_USERNAME=username
export MAIL_PASSWORD=password
```

#### Run it
``` 
cd src
python app.py
```