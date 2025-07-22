# {{cookiecutter.project_name}}

<a target="_blank" href="https://cookiecutter-data-science.drivendata.org/">
    <img src="https://img.shields.io/badge/CCDS-Project%20template-328F97?logo=cookiecutter" />
</a>

{{cookiecutter.description}}

## Project Organization

```
├── .env               <- File for storing environment variables, which can be loaded using
│                         python-dotenv and used in your module/notebooks
│                         Note: ignored by .gitignore; _do not_ add or commit this file with git
├── LICENSE            <- Open-source license
├── Makefile           <- Makefile with convenience commands like `make data` or `make build`
├── README.md          <- The top-level README for developers using this project.
│
├── data               <- Directory for saving local copies of datasets and/or temporary datasets
│
├── docs               <- Directory for any other supporting documentation beyond the README
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
        ├── datasets.py             <- Scripts to download or generate data
        │
        └── plots.py                <- Code to create visualizations
```

--------
