import shutil
from copy import copy
from pathlib import Path

from yaml import load, dump
import tomlkit
try:
    from yaml import CLoader as Loader, CDumper as Dumper
except ImportError:
    from yaml import Loader, Dumper

# https://github.com/cookiecutter/cookiecutter/issues/824
#   our workaround is to include these utility functions in the CCDS package
from ccds.hook_utils.custom_config import write_custom_config
from ccds.hook_utils.dependencies import (
    basic,
    packages,
    ruff,
    scaffold,
    # build_deps,
    write_dependencies,
    write_python_version,
)

build_deps = [
    "build",
    "setuptools-scm",
]

scaffold_deps = [
    "sqlalchemy",
    "psycopg2",
    "jupyter"
]

#
#  TEMPLATIZED VARIABLES FILLED IN BY COOKIECUTTER
#
packages_to_install = copy(packages)

# {% if cookiecutter.include_code_scaffold == "Yes" %}
# packages_to_install += scaffold
packages_to_install += scaffold_deps
# {% endif %}

# {% if cookiecutter.pydata_packages == "basic" %}
packages_to_install += basic
# {% endif %}

dev_packages_to_install = ruff + build_deps

# track packages that are not available through conda
pip_only_packages = [ ]

# track equivalent packages that are available through conda
conda_package_aliases = {
    "build": "conda-build",
    "setuptools-scm": "conda-forge::setuptools-scm",
}

if "{{ cookiecutter.dependency_file }}" == "environment.yml":
    packages_to_install = [conda_package_aliases.get(p, p) for p in packages_to_install if p not in pip_only_packages]
    dev_packages_to_install = [conda_package_aliases.get(p, p) for p in dev_packages_to_install if p not in pip_only_packages]

# Use the selected documentation package specified in the config,
# or none if none selected
docs_path = Path("docs")
packages_to_install += ["mkdocs"]
pip_only_packages += ["mkdocs"]
docs_subpath = docs_path / "mkdocs"
for obj in docs_subpath.iterdir():
    shutil.move(str(obj), str(docs_path))

# Remove all remaining docs templates
for docs_template in docs_path.iterdir():
    if docs_template.is_dir() and not docs_template.name == "docs":
        shutil.rmtree(docs_template)

#
#  POST-GENERATION FUNCTIONS
#
write_dependencies(
    "{{ cookiecutter.dependency_file }}",
    packages_to_install,
    pip_only_packages,
    repo_name="{{ cookiecutter.repo_name }}",
    module_name="{{ cookiecutter.module_name }}",
    python_version="{{ cookiecutter.python_version_number }}",
    # conda_package_aliases=conda_package_aliases,
    # dev_packages=dev_packages_to_install
)

if "{{ cookiecutter.dependency_file }}" == "pyproject.toml":
    with open("pyproject.toml", "r") as f:
        doc = tomlkit.parse(f.read())
    doc["dependency-groups"].add("dev", sorted(dev_packages_to_install))

    with open("pyproject.toml", "w") as f:
        f.write(tomlkit.dumps(doc))
    Path("meta.yaml").unlink() # Remove unused meta.yml file
elif "{{ cookiecutter.dependency_file }}" == "environment.yml":
    with open("meta.yaml", "r") as f:
        doc = load(f.read(), Loader=Loader)
    # TODO: Maybe just plug in values from pyproject.toml directly in the yaml, e.g.
    # https://docs.conda.io/projects/conda-build/en/latest/resources/define-metadata.html#loading-data-from-other-files
    python_string = "python={{ cookiecutter.python_version_number}}"
    doc['requirements']['build'] += [python_string]
    doc['requirements']['build'] += dev_packages_to_install
    doc['requirements']['run'] += [python_string]
    doc['requirements']['run'] += packages_to_install

    with open("meta.yaml", "w") as f:
        f.write(dump(doc, Dumper=Dumper))

write_python_version("{{ cookiecutter.python_version_number }}")

write_custom_config("{{ cookiecutter.custom_config }}")

# Make single quotes prettier
# Jinja tojson escapes single-quotes with \u0027 since it's meant for HTML/JS
pyproject_text = Path("pyproject.toml").read_text()
Path("pyproject.toml").write_text(pyproject_text.replace(r"\u0027", "'"))

# {% if cookiecutter.include_code_scaffold == "No" %}
# remove everything except __init__.py so result is an empty package
for generated_path in Path("src/{{ cookiecutter.module_name }}").iterdir():
    if generated_path.is_dir():
        shutil.rmtree(generated_path)
    elif generated_path.name != "__init__.py":
        generated_path.unlink()
    elif generated_path.name == "__init__.py":
        # remove any content in __init__.py since it won't be available
        generated_path.write_text("")
# {% endif %}
