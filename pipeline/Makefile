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

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

install: ## Install requirements
	pip install --no-cache-dir -r requirements.txt

build: clean ## Build egg
	scrapyd-deploy --build-egg=output.egg

deploy: build ## Deploy spiders
	while ! curl -L -s "http://scrapyd:6800/"; do sleep 0.1; done
	while ! curl -L -s "http://spiderkeeper:5000/"; do sleep 0.1; done
	curl -vvv -L -u admin:admin -c /tmp/cookies -b /tmp/cookies "http://spiderkeeper:5000/project/create" -d "project_name=pipeline"
	curl -vvv -L -u admin:admin -c /tmp/cookies -b /tmp/cookies -F "file=@output.egg" "http://spiderkeeper:5000/project/1/spider/upload"

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

lint: ## check style with flake8
	flake8
