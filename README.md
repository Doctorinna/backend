# Doctorinna-Backend

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/25574ca8ef4a46cd95510e17560949ac)](https://app.codacy.com/gh/Doctorinna/backend?utm_source=github.com&utm_medium=referral&utm_content=Doctorinna/backend&utm_campaign=Badge_Grade_Settings)

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

## Start server
When the environment is ready, run the server by typing in prompt from the project directory:
```
python manage.py runserver
```


