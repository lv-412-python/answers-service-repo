.PHONY: help install clear lint dev-env prod-env
PYTHON_PATH_ANSWERS_SERVICE := /home/lev/project/4m/4m-answers-service/answers_service
.DEFAULT: help
help:
	@echo "make install"
	@echo "       creates venv and installs requirements"
	@echo "make dev-env"
	@echo "       run project in dev mode"
	@echo "make prod-env"
	@echo "       run project in production mode"
	@echo "make lint"
	@echo "       run pylint"
	@echo "make clear"
	@echo "       deletes venv and .pyc files"

install:
	python3 -m venv venv
	. /home/lev/project/4m/4m-answers-service/venv/bin/activate; \
	pip install setuptools --upgrade --ignore-installed --user
	pip install pip --upgrade --ignore-installed --user
	pip install -r requirements.txt --user;

clear:
	rm -rf venv
	find -iname "*.pyc" -delete

dev-env:
	 make install; \
	 export PYTHONPATH=$(PYTHON_PATH_ANSWERS_SERVICE);\
	 export FLASK_APP="setup.py"; \
	 export FLASK_ENV="development"; \
	 flask run --port=5000;


prod-env:
	 make install; \
	 export PYTHONPATH=$(PYTHON_PATH_ANSWERS_SERVICE); \
	 export FLASK_APP="setup.py"; \
	 export FLASK_ENV="production"; \
	 flask run --port=5000;

lint:
	pylint setup.py answers_service/