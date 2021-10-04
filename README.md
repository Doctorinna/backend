# Doctorinna-Backend

> This is the part of the Doctorinna project, check out the [overview repository](https://github.com/Doctorinna/overview) first

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/924cfbae7cbd4c889eca950aa645a362)](https://www.codacy.com/gh/Doctorinna/backend/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Doctorinna/backend&amp;utm_campaign=Badge_Grade)
[![codecov.io](https://codecov.io/github/Doctorinna/backend/coverage.svg?branch=dev)](https://app.codecov.io/gh/Doctorinna/backend?branch=dev)

This repository is place for Doctorinna API. It is built on the Django REST Framework. Current version is project skeleton with `risk_factors` microservice. 

Later this microservice will be used to 
-   send list of questions 
-   accept user answers
-   calculate risk factors using ML model
-   perform analytics of the result
-   give recommendation on lifestyle
-   interact with databases of questions and results

## Getting started
Backend is written in Python programming language. In order to launch it locally, one needs to install interpreter from [the official website](https://www.python.org/downloads/). \
In order to check that it was installed correctly, type `python --version`. The python version should be displayed.\
Once the interpreter is ready, install all the dependencies by typing in prompt from the project directory:
```
pip install -r requirements.txt
```
The project utilizes Docker Compose tool used for running multi-container Docker applications. It relies on Docker engine that can be installed by following [official instructions](https://docs.docker.com/engine/install/). Once the engine installed proceed with installation of Docker Compose. For the details see [official guidelines](https://docs.docker.com/compose/install/). 

## Run application server
The API might be launched directly on your machine using localhost or using docker containers. Following sections describe these options. 

### For development
If you want to contribute to the project it is best to set up the environment in the same way as the developers.
To do so, start with running Postgre SQL in Docker container. The engine uses default parameters of database name, user and password. Configure them in `.env` file.
Define and run the Docker container in project's root directory using:
```
docker-compose -f database.yml up
```
Note that it will serve on port 5432 that is convention for PostgreSQL. 

Next step is to change the default host for database in [settings.py](backend/backend/settings.py). 
Intended that for average user it is more convenient to run application via Docker compose that creates aliases inside the network. By default, this alias is the name of database container. 
Since we do not have network outside the container this alias will fail, so go to settings file, and find declaration `DATABASES` and change value of `HOST` to `'localhost'`. 

When the environment is ready, run the server by typing in prompt from the project directory:
```
python ./backend/manage.py runserver
```
Apparently, you need to run the application locally without containerization.

### For testing
If you want to build containers from source code, this option is probably for you. \
Use following command in terminal:  
```
docker-compose up -d
```
This can be helpful, if you want to test your code without reference to the operating system and environment. 
Because there is used `nginx`, the server will be available on port 80, i.e. default HTTP port.

### Using images
The most handy option is to compose ready-to-use images for each container.
```
docker-compose -f dockerhub.yml up -d
```
However, these images are latest created, so there can be problems with some functionalities. 
The Docker compose file with [stable version](https://github.com/Doctorinna/overview/blob/master/docker-compose.yml) is available in our overview repository.
