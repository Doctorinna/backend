<div align="center">
  <img src="./media/Logotype.svg" alt="Logotype"/><br/>
  <h1> API Doctorinna </h1>
  <p></p>
</div>

> This is the part of the Doctorinna project, check out the [overview repository](https://github.com/Doctorinna/overview) first

[![Codacy Badge](https://app.codacy.com/project/badge/Grade/924cfbae7cbd4c889eca950aa645a362)](https://www.codacy.com/gh/Doctorinna/backend/dashboard?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=Doctorinna/backend&amp;utm_campaign=Badge_Grade)
[![codecov.io](https://codecov.io/github/Doctorinna/backend/coverage.svg?branch=master)](https://app.codecov.io/gh/Doctorinna/backend?branch=master)
[![CI/CD master](https://github.com/Doctorinna/backend/actions/workflows/ci-cd-master.yml/badge.svg)](https://github.com/Doctorinna/backend/actions/workflows/ci-cd-master.yml)

This repository is place for Doctorinna API. Our long-term goal is to create an [open-source API](http://3.128.254.206) that provides analysis of a variety of medical data. We want to solve a whole range of problems related to the digitalization of medicine. In particular, the shortage of doctors in third world countries, and the high cost of solutions for the analysis of biomedical data. For example, based on this API, applications for self-analysis of health in third world countries can be developed. 

We started our work with the development of a microservice to identify risk groups. The analysis is based on questions that do not require medical measurements. More details are provided in the [readme file](backend/risk_factors/README.md) for `risk_factors` microservice.

## ⚡ Getting started
Backend is written in Python programming language. In order to launch it locally, one needs to install interpreter from [the official website](https://www.python.org/downloads/). In order to check that it was installed correctly, type `python --version`. The python version should be displayed.

The project utilizes Docker Compose tool used for running multi-container Docker applications. It relies on Docker engine that can be installed by following [official instructions](https://docs.docker.com/engine/install/). Once the engine installed proceed with installation of Docker Compose. For the details see [guidelines](https://docs.docker.com/compose/install/). 

### Technical stack
The API utilizes various technologies to provide stability, scalability, and high performance, including:
1. Django REST Framework
2. PostgreSQL
3. Docker
4. Nginx
5. Gunicorn
6. RabbitMQ
7. Celery
8. Scikit-learn
9. Swagger

## 🐳 Run application server
The API might be launched directly on your machine using localhost or within the docker containers. Following sections describe these options. 

### For development
If you want to contribute to the project it is best to set up the environment in the same way as the developers.
To do so, start with installation of all the dependencies by typing in prompt from the project directory:
```
pip install -r requirements.txt
```
Further, run PostgreSQL RDBMS and message-broker RabbitMQ in Docker container. The engine uses default parameters of database name, user and password. Configure them in `.env` file.
Create and run the Docker container in project's root directory using:
```
docker-compose -f database.yml up
```
When the environment is ready, run the server by typing in prompt from the project directory:
```
python ./backend/manage.py runserver
```

### Prerequisites
It is necessary to configure the [.env file](./.env) before following sections. Pay attention that `POSTGRES_HOST`, `BROKER_HOST` are given by default.

### For testing
If you want to build containers from source code, this option is probably for you. \
Use following command in terminal:  
```
docker-compose up -d
```
This can be helpful, if you want to test your code without reference to the operating system and environment. 
The end system uses `nginx` that configures proxy to the application server, so that it is available on port `80`, i.e. default HTTP port.

### Using images
The most handy option is to compose ready-to-use images for each container. Use the following command to compose containerized application on your machine:
```
docker-compose -f dockerhub.yml up -d
```
Note that images used for build are latest created by CI/CD pipeline on dev branch. For this reason, there can occur problems with functionalities. 
The Docker compose file with [stable version](https://github.com/Doctorinna/overview/blob/master/docker-compose.yml) is available in our overview repository.

## ✏️ How to contribute?
This application follows the modular architecture admitted by Django community.
You are expected to create a reusable application containing at least 3 layers: serializer, view set, and router. This application should allow for biomedical analysis. Any tool is accepted, starting from the segmentation of medical images, ending with the diagnosis of diseases by symptoms.

First, make a fork of this repository, and develop your own tool. Make sure it is error-free and the test coverage is at least 60 percent. Update `docker-compose` files accordingly, and check their operability. 

Further, send a pull request. In the comment, write the main features of the tool, the technology stack used, and a brief description of the algorithms. This should be enough for us to accept your code.

> To check the quality of the code, we use `flake8` and `codacy`.

## 📖 API Documentation
The documentation for Doctorinna API is available [online](http://3.128.254.206) on home `/ route`. It is generated by Swagger and all requests are interactive. 


## 🔓 Deployments
For continuous deployment there are used AWS EC2 instances. API is available in two versions:
1.  [Development version](http://18.216.235.168) - contains build of `dev` branch
2.  [Stable version](http://3.128.254.206) - contains build of `master` branch

### Docker-hub images
Versions of docker images are available online:
1. [API + gunicorn](https://registry.hub.docker.com/repository/docker/aldanis/doctorinna-api)
2. [Nginx server](https://registry.hub.docker.com/repository/docker/aldanis/doctorinna-nginx)

## 💻 Contributors
**Danis Alukaev** <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Email: <a>d.alukaev@innopolis.university</a> <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GitHub: <a href="https://github.com/DanisAlukaev">@DanisAlukaev</a> <br>    

**Lada Morozova** <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Email: <a>l.morozova@innopolis.university</a> <br>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; GitHub: <a href="https://github.com/ladamoroz">@ladamoroz</a> <br>    
## 📃 Licence
`Doctorinna API` is free and open-source software licensed under the [MIT License](LICENSE).