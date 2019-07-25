.PHONY: help install install-requirements clear run-dev-mode run-prod-mode lint
PYTHON_PATH_ANSWERS_SERVICE :=  answers_service
.DEFAULT: help
help:
	@echo "make install"
	@echo "       creates venv and installs requirements"
	@echo "make install-requirements"
	@echo "       installs requirements"
	@echo "make run-dev-mode"
	@echo "       run project in dev mode"
	@echo "make run-prod-mode"
	@echo "       run project in production mode"
	@echo "make lint"
	@echo "       run pylint"
	@echo "make clear"
	@echo "       deletes venv and .pyc files"

install:
	python3 -m venv venv
	. venv/bin/activate; \
	pip install setuptools --upgrade; \
	pip install pip --upgrade; \
	pip install -r requirements.txt;

install-requirements:
	 pip3 install -r requirements.txt;

clear:
	rm -rf venv
	find -iname "*.pyc" -delete

run-dev-mode:
	 . venv/bin/activate; \
	 export PYTHONPATH=$(PYTHON_PATH_ANSWERS_SERVICE); \
	 export FLASK_APP="setup.py"; \
	 export FLASK_ENV="development"; \
	 flask run --port=5050;

run-prod-mode:
	 . venv/bin/activate; \
	 export PYTHONPATH=$(PYTHON_PATH_ANSWERS_SERVICE); \
	 export FLASK_APP="setup.py"; \
	 export FLASK_ENV="production"; \
	 flask run --port=5050;

lint:
	. venv/bin/activate; \
	pylint setup.py answers_service/