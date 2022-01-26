# Export application env vars
include deploy/.env
export

PROJECT_NAME := balance
PROJECT_SRC := app

IMAGE_NAME := $(PROJECT_NAME)
APP_CONTAINER_NAME := $(PROJECT_SRC)

DOCKER := env docker
PYTHON := env python3
COMPOSE := env docker-compose


run:
	$(COMPOSE) up -d

build:
	$(COMPOSE) build

stop:
	$(COMPOSE) stop

del:
	$(DOCKER) rm $(PROJECT_SRC)
	$(DOCKER) rmi $(PROJECT_NAME)

config:
	cat deploy/.env

lint:
	$(PYTHON) -m flake8 $(PROJECT_SRC)

cs:
	$(PYTHON) -m black $(PROJECT_SRC)

test:
	$(PYTHON) -m pytest -vv

test-cov:
	$(PYTHON) -m pytest -vv --cov=$(PROJECT_SRC)

test-cov-html: test
	$(PYTHON) -m coverage html
	$(PYTHON) -m webbrowser htmlcov/index.html

req:
	pip install -r requirements.txt
	pip install -r requirements.dev.txt
