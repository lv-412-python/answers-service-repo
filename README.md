# Answers service [![Build Status](https://travis-ci.org/lv-412-python/answers-service-repo.svg?branch=develop)](https://travis-ci.org/lv-412-python/answers-service-repo) 
## Description
This is the source code of the answers service, part of 4m project. This service stores and output answers on the Web page

## Technologies
* Python (3.6.8)
* Flask (1.0.3)
* PostgreSQL (10.8)
* Docker

## Install
For the next steps of service installation, you will need setup of Ubuntu 18.04, and Docker

### Install and configure PostgreSQL server on your local machine:
```
sudo apt-get install postgresql postgresql-contrib
sudo -u postgres psql postgres

postgres=# \password
Enter new password:
Enter it again:

postgres=# CREATE DATABASE your_custom_db_name;

postgres=# \q
```
```
sudo apt-get install python3-pip
sudo pip3 install virtualenv 
```

### In the project root create venv and install requirements with Make
```
make install

### Run project

#### run in development mode
```
make run-dev-mode
```

#### run in production mode
```
make run-prod-mode
```
#### Create docker image
```
docker build -t answers-service:latest .
```
#### Run docker container
```
docker run -d -t 5050:5050 answers-service:latest
```

## Project team:
* **Lv-412.WebUI/Python team**:
    - @sikyrynskiy
    - @olya_petryshyn
    - @taraskonchak
    - @OlyaKh00
    - @ement06
    - @iPavliv
    - @Anastasia_Siromska
    - @romichh