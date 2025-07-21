# Cookiecutter Data Science

_A logical, reasonably standardized but flexible project structure for doing and sharing data science work._

[![PyPI - Version](https://img.shields.io/pypi/v/cookiecutter-data-science)](https://pypi.org/project/cookiecutter-data-science/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/cookiecutter-data-science)](https://pypi.org/project/cookiecutter-data-science/)
<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>
[![tests](https://github.com/drivendataorg/cookiecutter-data-science/actions/workflows/tests.yml/badge.svg)](https://github.com/drivendataorg/cookiecutter-data-science/actions/workflows/tests.yml)

**Cookiecutter Data Science (CCDS)** is a tool for setting up a data science project template that incorporates best practices. To learn more about CCDS's philosophy, visit the [project homepage](https://cookiecutter-data-science.drivendata.org/).

> ℹ️ Cookiecutter Data Science v2 has changed from v1. It now requires installing the new cookiecutter-data-science Python package, which extends the functionality of the [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/README.html) templating utility. Use the provided `ccds` command-line program instead of `cookiecutter`.

## Installation

Cookiecutter Data Science v2 requires Python 3.9+. Since this is a cross-project utility application, we recommend installing it with [pipx](https://pypa.github.io/pipx/). Installation command options:

```bash
# With pipx from PyPI (recommended)
pipx install cookiecutter-data-science

# With pip from PyPI
pip install cookiecutter-data-science

# With conda from conda-forge (coming soon)
# conda install cookiecutter-data-science -c conda-forge
```

## Starting a new project

To start a new project, run:

```bash
ccds
```

### The resulting directory structure

The directory structure of your new project will look something like this (depending on the settings that you choose):

```
├── LICENSE            <- Open-source license
├── Makefile           <- Makefile with convenience commands like `make data` or `make build`
├── README.md          <- The top-level README for developers using this project.
│
├── data               <- Directory for saving local copies of datasets and/or temporary datasets
│
├── docs               <- A default mkdocs project; see www.mkdocs.org for details
│
├── notebooks          <- Jupyter notebooks. Naming convention is a number (for ordering),
│                         the creator's initials, and a short `-` delimited description, e.g.
│                         `1.0-jqp-initial-data-exploration`.
│
├── pyproject.toml     <- Project configuration file with package metadata for
│                         {{ cookiecutter.module_name }} and configuration for tools like ruff
│
├── references         <- Data dictionaries, manuals, and all other explanatory materials.
│
├── visualizations     <- Generated analysis as HTML, PDF, LaTeX, etc.
│   └── figures        <- Generated graphics and figures to be used in visualizations
│
├── requirements.txt   <- The requirements file for reproducing the analysis environment, e.g.
│                         generated with `pip freeze > requirements.txt`
│
└── src                <- Source code for use in this project.
    │
    └── {{ cookiecutter.module_name }}   <- Source code for use in this project.
        │
        ├── __init__.py             <- Makes {{ cookiecutter.module_name }} a Python module
        │
        ├── config.py               <- Store useful variables and configuration
        │
        ├── datasets.py              <- Scripts to download or generate data
        │
        └── plots.py                <- Code to create visualizations
```

## Using unreleased changes

By default, `ccds` will use the _project template_ version that corresponds to the _installed `ccds` package_ version (e.g., if you have installed `ccds` v2.0.1, you'll use the v2.0.1 version of the project template by default). To use a specific version of the project template, use the `-c/--checkout` flag to provide the branch (or tag or commit hash) of the version you'd like to use. For example to use the project template from the `master` branch:

```bash
ccds -c master
```

## Using v1

If you want to use the old v1 project template, you need to have either the cookiecutter-data-science package or cookiecutter package installed. Then, use either command-line program with the `-c v1` option:

```bash
ccds https://github.com/drivendataorg/cookiecutter-data-science -c v1
# or equivalently
cookiecutter https://github.com/drivendataorg/cookiecutter-data-science -c v1
```

## Contributing

We welcome contributions! [See the docs for guidelines](https://cookiecutter-data-science.drivendata.org/contributing/).

### Installing development requirements

```bash
pip install -r dev-requirements.txt
```

### Running the tests

```bash
pytest tests
```
