# Targets
BUILD_NUMBER ?= 0
DOCKER_IMAGE_NAME ?= "pyhtmx"
SHORT_HASH := $(shell git rev-parse --short HEAD)
SHELL := /bin/bash

.PHONY: checkstyle clear codestyle help install test env
.DEFAULT_GOAL := help

clear: ## Clear all build files and folders
	rm -rf dist build *.egg-info .env cache

codestyle: ## Apply codestyle
	@source .env/bin/activate; \
		ruff . --fix; \
		isort .;

run: ## Execute the service locally
	@source .env/bin/activate; \
		scripts/run.sh

help: ## Display this help
	@awk 'BEGIN {FS = ":.*##"; printf "\nUsage:\n  make \033[36m\033[0m\n\nTargets:\n"} /^[a-zA-Z_-]+:.*?##/ { printf "\033[36m%-12s\033[0m %s\n", $$1, $$2 }' $(MAKEFILE_LIST)

install: env ## Create a virtual environment and install package with all dependencies
	@source .env/bin/activate; \
		poetry config virtualenvs.create false; \
		poetry install

test: ## Run pytest against package
	@source .env/bin/activate; \
		scripts/run_tests.sh

env:
	@python3 -m venv .env
	@source .env/bin/activate \
		&& pip install -qU pip \
		&& pip install -q "black>=23.9.1" "isort>=5.12.0" "poetry>=1.6.1" "pytest>=7.4.2" \
		&& poetry self add --quiet poetry-bumpversion@latest

check-%:
	@#$(or ${$*}, $(error $* is not set))

docker-build: ## Build docker image
	@docker build -t ${DOCKER_IMAGE_NAME}:${SHORT_HASH} --build-arg BUILD_NUMBER=${SHORT_HASH} --no-cache .

docker-stop: ## Stop docker image
	@docker stop ${DOCKER_IMAGE_NAME}

docker-remove: ## Remove docker image
	@docker rm -f ${DOCKER_IMAGE_NAME}

docker-run: ## Run docker image
	@docker run \
	--name pyhtmx \
	--restart always \
	-p 8000:80 \
	-e MAX_WORKERS=2 \
	-e PSQL__HOST="mirserver" \
	-e PSQL__PORT=5432 \
	-e PSQL__USER="htmx" \
	-e PSQL__PASSWORD="htmx123" \
	-e PSQL__DATABASE="pyhtmx" \
	-d pyhtmx:${SHORT_HASH}
# Aliases
.PHONY: i r t cl cs

db: docker-build
dr: docker-run
drr: docker-remove
ds: docker-stop
i: install
r: run
t: test
cl: clear
cs: codestyle
tw: tailwind