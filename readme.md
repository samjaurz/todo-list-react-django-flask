# TODO LIST ENDPOINT

The principal objective of this project is to implement a REST API with SOLID principles.
Manage the backend in Flask and Django. Independent of the technology, the endpoint must 
work with the client, in this case, it will be React with the framework of Next.js.

## ESSENCIALS 
  - Python
  - Git
  - Docker
  - Node

## Clone repositorio

First you need clone the repository, open a terminal and run the command
```
git clone https://github.com/samjaurz/todo-list-react-django-flask.git
cd todo-list-react-django-flask.git
```



## INSTALL DEPENDENCIES
if you don't have already poetry installed [Poetry](https://python-poetry.org/docs/) 

Check if you are in the carpet of the fields poetry.lock and pyproject.toml are.  
in the next route todo-list-react-django-flask/flask-api run the next command:
```
poetry install
```

### Activate environment  
MAC, LINUX
```
source .venv/bin/activate
```
WINDOWS 
```
.venv\Scripts\activate 
```

## DOCKER 
Setup for the Local database   
go to this path flask-api/docker and run this command for create the container:
```
docker-compose up -d
```

RUN APPLICATION

go to this path flask-api/backend/flask. and run the next command
```
python app.py
```

**Note:** if not find the backend module run pwd for get the route you are in and the modified the PYTHONPATH
```
export PYTHONPATH=/Users/sam/Desktop/try/todo-list-react-django-flask/flask-api:$PYTHONPATH
```
For Swagger documentation of the RESTAPI
```
http://localhost:5000/apidocs/
```