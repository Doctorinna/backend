# Doctorinna-Backend

> This is the part of the Doctorinna project, check out the [overview repository](https://github.com/Doctorinna/overview) first

This repository is place for Doctorinna API. It is built on the Django REST Framework. Current version is project skeleton with `risk_factors` microservice. 

Later this microservice will be used to 
- send list of questions 
- accept user answers
- calculate risk factors using ML model
- perform analytics of the result
- give recommendation on lifestyle
- interact with databases of questions and results

## Getting started:
Backend is written in Python programming language. In order to launch it locally, one needs to install interpreter from [the official website](https://www.python.org/downloads/). \
In order to check that it was installed correctly, type `python --version`. The python version should be displayed.\
Once the interpreter is ready, install all the dependencies by typing in prompt from the project directory:
```
pip install -r requirements.txt
```

The project utilizes Docker Compose tool used for running multi-container Docker applications. It relies on Docker engine that can be installed by following [official instructions](https://docs.docker.com/engine/install/). Once the engine installed proceed with installation of Docker Compose. For the details see [official guidelines](https://docs.docker.com/compose/install/). 

## Database server
The project uses PostgreSQL database. For convenience database is runned in Docker container. 
The engine uses default parameters of database name, user and password. Configure them in `.env` file.
Define and run the Docker container in project's root directory using:
```
docker-compose up
```
Note that it will serve on port 5432 that is convention for PostgreSQL. 

## Application server
When the environment is ready, run the server by typing in prompt from the project directory:
```
python manage.py runserver
```


