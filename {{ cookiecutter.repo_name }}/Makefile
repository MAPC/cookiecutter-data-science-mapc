#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = {{ cookiecutter.repo_name }}
PYTHON_VERSION = {{ cookiecutter.python_version_number }}
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

{% if cookiecutter.dependency_file != 'none' %}
## Install Python dependencies
.PHONY: requirements
requirements:
	{% if "requirements.txt" == cookiecutter.dependency_file -%}
	{% if "uv" == cookiecutter.environment_manager -%}
	uv pip install -r requirements.txt
	{% else -%}
	$(PYTHON_INTERPRETER) -m pip install -U pip
	$(PYTHON_INTERPRETER) -m pip install -r requirements.txt
	{% endif -%}
	{% elif "pyproject.toml" == cookiecutter.dependency_file -%}
	{% if "uv" == cookiecutter.environment_manager -%}
	uv sync
	{% else -%}
	pip install -e .
	{% endif -%}
	{% elif "environment.yml" == cookiecutter.dependency_file -%}
	conda env update --name $(PROJECT_NAME) --file environment.yml --prune
	{% elif "Pipfile" == cookiecutter.dependency_file -%}
	pipenv install
{% endif %}
{% endif %}


## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete

## Lint using ruff (use `make format` to do formatting)
.PHONY: lint
lint:
	ruff format --check
	ruff check

## Format source code with ruff
.PHONY: format
format:
	ruff check --fix
	ruff format

## Build the Python package for distribution
.PHONY: build
build:
	{% if cookiecutter.dependency_file != 'none' %}
	{% if "uv" == cookiecutter.environment_manager -%}
	uv sync --group dev
	python -m build
	{% elif "conda" == cookiecutter.environment_manager -%}
	@echo ">>> Temporarily adding build tools to conda env..."
	conda install --name ${PROJECT_NAME} conda-forge::conda-build
	conda-build . --output-folder dist/
	@echo ">>> Restoring conda env to dependencies from environment.yml..."
	conda env update --name $(PROJECT_NAME) --file environment.yml --prune
	{% endif -%}
	{% endif -%}

{% if cookiecutter.environment_manager != 'none' %}
## Set up Python interpreter environment
.PHONY: create_environment
create_environment:
	{% if cookiecutter.environment_manager == 'conda' -%}
	{% if cookiecutter.dependency_file != 'environment.yml' %}
	conda create --name $(PROJECT_NAME) python=$(PYTHON_VERSION) -y
	{% else -%}
	conda env create --name $(PROJECT_NAME) -f environment.yml
	{% endif %}
	@echo ">>> conda env created. Activate with:\nconda activate $(PROJECT_NAME)"
	{% elif cookiecutter.environment_manager == 'virtualenv' -%}
	@bash -c "if [ ! -z `which virtualenvwrapper.sh` ]; then source `which virtualenvwrapper.sh`; mkvirtualenv $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); else mkvirtualenv.bat $(PROJECT_NAME) --python=$(PYTHON_INTERPRETER); fi"
	@echo ">>> New virtualenv created. Activate with:\nworkon $(PROJECT_NAME)"
	{% elif cookiecutter.environment_manager == 'pipenv' -%}
	pipenv --python $(PYTHON_VERSION)
	@echo ">>> New pipenv created. Activate with:\npipenv shell"
	{% elif cookiecutter.environment_manager == 'uv' -%}
	uv venv --python $(PYTHON_VERSION)
	@echo ">>> New uv virtual environment created. Activate with:"
	@echo ">>> Windows: .\\\\.venv\\\\Scripts\\\\activate"
	@echo ">>> Unix/macOS: source ./.venv/bin/activate"
{% endif %}
{% endif %}


#################################################################################
# PROJECT RULES                                                                 #
#################################################################################

{% if cookiecutter.include_code_scaffold == 'Yes' %}
## Make datasets
.PHONY: data
data: requirements
	$(PYTHON_INTERPRETER) {{ cookiecutter.module_name }}/datasets.py
{% endif %}

#################################################################################
# Self Documenting Commands                                                     #
#################################################################################

.DEFAULT_GOAL := help

define PRINT_HELP_PYSCRIPT
import re, sys; \
lines = '\n'.join([line for line in sys.stdin]); \
matches = re.findall(r'\n## (.*)\n[\s\S]+?\n([a-zA-Z_-]+):', lines); \
print('Available rules:\n'); \
print('\n'.join(['{:25}{}'.format(*reversed(match)) for match in matches]))
endef
export PRINT_HELP_PYSCRIPT

help:
	@$(PYTHON_INTERPRETER) -c "${PRINT_HELP_PYSCRIPT}" < $(MAKEFILE_LIST)
