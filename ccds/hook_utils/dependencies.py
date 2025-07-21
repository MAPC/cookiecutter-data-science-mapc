import tomlkit

packages = [
    "pip",
    "python-dotenv",
]

ruff = ["ruff"]

basic = [
    "ipython",
    "jupyterlab",
    "matplotlib",
    "notebook",
    "numpy",
    "pandas",
    "scikit-learn",
]

scaffold = [
    "typer",
    "loguru",
    "tqdm",
    "sqlalchemy"
]

build = [
    "build",
    "setuptools-scm",
]


def resolve_python_version_specifier(python_version):
    """Resolves the user-provided Python version string to a version specifier.

    Examples:

    User provides: 3.12
    Resolved version specifier: ~=3.12.0
    Compatible versions: 3.12.0, 3.12.1, 3.12.2, etc.

    User provides: 3.12.2
    Resolved version specifier: ==3.12.2
    Compatible versions: 3.12.2

    See https://packaging.python.org/en/latest/specifications/version-specifiers/#compatible-release
    """
    version_parts = python_version.split(".")
    if len(version_parts) == 2:
        major, minor = version_parts
        patch = "0"
        operator = "~="
    elif len(version_parts) == 3:
        major, minor, patch = version_parts
        operator = "=="
    else:
        raise ValueError(
            f"Invalid Python version specifier {python_version}. "
            "Please specify version as <major>.<minor> or <major>.<minor>.<patch>, "
            "e.g., 3.10, 3.10.1, etc."
        )

    resolved_python_version = ".".join((major, minor, patch))
    return f"{operator}{resolved_python_version}"


def write_python_version(python_version):
    with open("pyproject.toml", "r") as f:
        doc = tomlkit.parse(f.read())

    doc["project"]["requires-python"] = resolve_python_version_specifier(python_version)
    with open("pyproject.toml", "w") as f:
        f.write(tomlkit.dumps(doc))


def write_dependencies(
    dependencies, packages, pip_only_packages, repo_name, module_name, python_version, conda_package_aliases, dev_packages
):
    if dependencies == "pyproject.toml":
        with open(dependencies, "r") as f:
            doc = tomlkit.parse(f.read())
        doc["project"].add("dependencies", sorted(packages))
        doc["dependency-groups"].add("dev", sorted(dev_packages))
        doc["project"]["dependencies"].multiline(True)

        with open(dependencies, "w") as f:
            f.write(tomlkit.dumps(doc))

    elif dependencies == "environment.yml":
        with open(dependencies, "w") as f:
            lines = [
                f"name: {repo_name}",
                "channels:",
                "  - conda-forge",
                "dependencies:",
            ]

            lines += [f"  - python={python_version}"]
            lines += [f"  - {conda_package_aliases.get(p, p)}" for p in packages+dev_packages if p not in pip_only_packages]

            lines += ["  - pip:"]
            lines += [f"    - {p}" for p in packages if p in pip_only_packages]
            lines += ["    - -e ."]

            f.write("\n".join(lines))
