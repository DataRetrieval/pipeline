.PHONY: install clean clean-pyc clean-build help
.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT

define DEPLOY_BASHSCRIPT
	while ! curl -s "http://scrapyd:6800/"; do sleep 0.1; done
	while ! curl -s "http://spiderkeeper:5000/"; do sleep 0.1; done
	if ! curl -s http://scrapyd:6800/listprojects.json | grep -q '"pipeline"'; then
		curl -u "${SPIDERKEEPER_USERNAME}:${SPIDERKEEPER_PASSWORD}" http://spiderkeeper:5000/project/create -d "project_name=pipeline"
	fi
	curl -u "${SPIDERKEEPER_USERNAME}:${SPIDERKEEPER_PASSWORD}" -F file=@output.egg http://spiderkeeper:5000/project/1/spider/upload
endef
export DEPLOY_BASHSCRIPT

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

install: ## Install requirements
	pip install --no-cache-dir -r requirements.txt

build: clean ## Build egg
	scrapyd-deploy --build-egg=output.egg

test: ## Check spiders contracts
	scrapy check

deploy: build ## Deploy spiders
	@bash -c "$$DEPLOY_BASHSCRIPT"

clean: clean-build clean-pyc ## remove all build and Python artifacts

clean-build: ## remove build artifacts
	find . -name 'build' -exec rm -fr {} +
	find . -name 'dist' -exec rm -fr {} +
	find . -name 'eggs' -exec rm -fr {} +
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

lint: ## check code with pylint
	pylint pipeline
