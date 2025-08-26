#TODO LIST ENDPOINT

The principal objective of this project is to implement a REST API with SOLID principles.
Manage the backend in Flask and Django. Independent of the technology, the endpoint must 
work with the client, in this case, it will be React with the framework of Next.js.

##ESSENCIALS 
-Python
-Git
-Docker
-Node

##Clone repositorio

First you need clone the repository, open a terminal and run the command
```
git clone https://github.com/samjaurz/todo-list-react-django-flask.git
cd todo-list-react-django-flask.git
```

if you don't have already poetry installed [Poetry](https://python-poetry.org/docs/)

##INSTALL DEPENDENCIES
Check if you are in the carpet of the fields poetry.lock and pyproject.toml are. run the next command:
in the next route todo-list-react-django-flask/flask-api
```
poetry install
```

activate entorne 
MAC, LINUX
```
source .venv/bin/activate
```
WINDOWS 
```
.venv\Scripts\activate 
```

DOCKER 
Local database 
go to this path flask-api/docker and run this command for create the container of the database
```
docker-compose up -d
```

go to this path flask-api/backend/flask. and run the next command
```
python app.py
```

if not find the backend module run the next command for get the route you are in 
```
pwd 
```
and the modified the PYTHONPATH
```
export PYTHONPATH=/Users/sam/Desktop/try/todo-list-react-django-flask/flask-api:$PYTHONPATH
```