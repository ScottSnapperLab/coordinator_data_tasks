.PHONY: clean clean-test clean-pyc clean-build docs help
.DEFAULT_GOAL := help

CONDA_ENV_NAME = data_tasks
CONDA_ROOT = $(shell conda info --root)
CONDA_ENV_DIR = $(CONDA_ROOT)/envs/$(CONDA_ENV_NAME)
CONDA_ENV_PY = $(CONDA_ENV_DIR)/bin/python

ifeq (,$(shell which conda))
HAS_CONDA=False
else
HAS_CONDA=True
endif


ifeq (${CONDA_DEFAULT_ENV},$(CONDA_ENV_NAME))
PROJECT_CONDA_ACTIVE=True
else
PROJECT_CONDA_ACTIVE=False
endif




define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

## alias for show-help
help: show-help

## remove all build, test, coverage and Python artifacts
clean: clean-build clean-pyc clean-test 


## remove build artifacts
clean-build: 
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

## remove Python file artifacts
clean-pyc: 
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

## remove test and coverage artifacts
clean-test: 
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

## check style with flake8
lint: 
	flake8 coordinator_data_tasks tests

## run tests quickly with the default Python
test: 
	pytest


## run tests on every Python version with tox
test-all: 
	tox

## check code coverage quickly with the default Python
coverage: 
	coverage run --source coordinator_data_tasks -m pytest
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

## generate Sphinx HTML documentation, including API docs
docs: 
	rm -f docs/coordinator_data_tasks.rst
	rm -f docs/modules.rst
	$(MAKE) -C docs clean
	$(MAKE) -C docs html
	$(BROWSER) docs/_build/html/index.html

## compile the docs watching for changes
servedocs: docs 
	watchmedo shell-command -p '*.rst' -c '$(MAKE) -C docs html' -R -D .

## package and upload a release
release: clean 
	python setup.py sdist upload
	python setup.py bdist_wheel upload

## builds source and wheel package
dist: clean 
	python setup.py sdist
	python setup.py bdist_wheel
	ls -l dist

## install the package to the active Python's site-packages
install: clean 
	python setup.py install


error_if_active_conda_env:
ifeq (True,$(PROJECT_CONDA_ACTIVE))
	$(error "This project's conda env is active." )
endif


## installs virtual environments and requirements
install-conda-env: 
ifeq ($(CONDA_ENV_PY), $(shell which python))
	@echo "Project conda env already installed."
else
	conda create -n $(CONDA_ENV_NAME) --file requirements.txt --yes  && \
	source activate $(CONDA_ENV_NAME) && \
	python -m ipykernel install --sys-prefix --name $(CONDA_ENV_NAME) --display-name "$(CONDA_ENV_NAME)" && \
	pip install -r requirements.pip.txt && \
	pip install -e .
endif


## installs requirements needed for development
install-dev-reqs:
	source activate $(CONDA_ENV_NAME) && \
	conda install --file requirements.dev.txt


## uninstalls virtual environments and requirements
uninstall-conda-env: 
	source activate $(CONDA_ENV_NAME); \
	rm -rf $$(jupyter --data-dir)/kernels/$(CONDA_ENV_NAME); \
	rm -rf $(CONDA_ENV_DIR)


#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

# Inspired by <http://marmelab.com/blog/2016/02/29/auto-documented-makefile.html>
# sed script explained:
# /^##/:
# 	* save line in hold space
# 	* purge line
# 	* Loop:
# 		* append newline + line to hold space
# 		* go to next line
# 		* if line starts with doc comment, strip comment character off and loop
# 	* remove target prerequisites
# 	* append hold space (+ newline) to line
# 	* replace newline plus comments by `---`
# 	* print line
# Separate expressions are necessary because labels cannot be delimited by
# semicolon; see <http://stackoverflow.com/a/11799865/1968>
.PHONY: show-help
## Show the available make targets
show-help:
	@echo "$$(tput bold)Available rules:$$(tput sgr0)"
	@echo
	@sed -n -e "/^## / { \
		h; \
		s/.*//; \
		:doc" \
		-e "H; \
		n; \
		s/^## //; \
		t doc" \
		-e "s/:.*//; \
		G; \
		s/\\n## /---/; \
		s/\\n/ /g; \
		p; \
	}" ${MAKEFILE_LIST} \
	| LC_ALL='C' sort --ignore-case \
	| awk -F '---' \
		-v ncol=$$(tput cols) \
		-v indent=19 \
		-v col_on="$$(tput setaf 6)" \
		-v col_off="$$(tput sgr0)" \
	'{ \
		printf "%s%*s%s ", col_on, -indent, $$1, col_off; \
		n = split($$2, words, " "); \
		line_length = ncol - indent; \
		for (i = 1; i <= n; i++) { \
			line_length -= length(words[i]) + 1; \
			if (line_length <= 0) { \
				line_length = ncol - indent - length(words[i]) - 1; \
				printf "\n%*s ", -indent, " "; \
			} \
			printf "%s ", words[i]; \
		} \
		printf "\n"; \
	}' \
	| more $(shell test $(shell uname) = Darwin && echo '--no-init --raw-control-chars')
