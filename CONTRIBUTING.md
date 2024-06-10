# Contributing

This guide explains how to set up the development environment, understand the project architecture, and follow the code style.

## Table of Contents

1. [Requirements](#requirements)
2. [Windows Support](#windows-support)
3. [Installation](#installation)
4. [Packaging](#packaging)
   - [Source Distribution](#source-distribution)
5. [Dependencies](#dependencies)
   - [Virtual Environments](#virtual-environments)
   - [Locking Dependencies](#locking-dependencies)
   - [Syncing Virtual Environments](#syncing-virtual-environments)
6. [Testing](#testing)
   - [Test Setup](#test-setup)
   - [Running Tests](#running-tests)
   - [Unit Testing](#unit-testing)
   - [Code Style Checking](#code-style-checking)
7. [Project Structure](#project-structure)
   - [Traditional Layout](#traditional-layout)
   - [Issues with the Traditional Layout](#issues-with-the-traditional-layout)
   - [Recommended Project Structure](#recommended-project-structure)
   - [Benefits of the src Layout](#benefits-of-the-src-layout)
8. [Contribution Process](#contribution-process)

## Requirements

- Python 3.9+

    > **Note:**
    >
    > Support for Python 2.7 in this project has been discontinued because [Python 2.7 support ended on January 1, 2020](https://pythonclock.org/).

## Windows Support

On Windows, use `py` instead of `python3` for many of the examples in this documentation.

This package fully supports Windows, along with Linux and macOS, but Python is typically [installed differently on Windows](https://docs.python.org/3/using/windows.html). Windows users typically access Python through the [py](https://www.python.org/dev/peps/pep-0397/) launcher rather than a `python3` link in their `PATH`. Within a virtual environment, all platforms operate the same and use a `python` link to access the Python version used in that virtual environment.

## Installation

To install and run the program without a development environment, follow these instructions:

1. Create and start the virtual environment (refer to the [Virtual Environments](#virtual-environments) section for more details):

    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

## Packaging

This project is designed as a Python package, meaning it can be bundled and redistributed as a single compressed file.

Packaging is configured by:

- `setup.py`
- `MANIFEST.in`

### Source Distribution

To package the project as a [source distribution](https://docs.python.org/3/distutils/sourcedist.html):

```bash
python3 setup.py sdist
```

This will generate `dist/cryptosteganography-0.0.1.tar.gz`.

(Note: The exact filename will vary based on the version number specified in `setup.py`.)

## Dependencies

Dependencies are defined in:

- `requirements.in`
- `requirements.txt`
- `dev-requirements.in`
- `dev-requirements.txt`

### Virtual Environments

It is best practice during development to create an isolated [Python virtual environment](https://docs.python.org/3/library/venv.html) using the `venv` standard library module. This will keep dependent Python packages from interfering with other Python projects on your system.

On Linux/macOS:

```bash
python3 -m venv venv
source venv/bin/activate
```

On Windows `cmd`:

```bash
py -m venv venv
venv\Scripts\activate.bat
```

Once activated, it is good practice to update `pip` to the latest version:

```bash
(venv)$ pip install --upgrade pip
```

### Locking Dependencies

This project uses [pip-tools](https://github.com/jazzband/pip-tools) to lock project dependencies and create reproducible virtual environments.

**Note:** *Library* projects should not lock their `requirements.txt`. Since `cryptosteganography` also has a CLI application, this end-user application example demonstrates how to lock application dependencies.

To update dependencies:

```bash
(venv)$ pip install pip-tools
(venv)$ pip-compile --output-file requirements.txt requirements.in
(venv)$ pip-compile --output-file dev-requirements.txt dev-requirements.in
```

### Syncing Virtual Environments

After generating or updating the requirements files, sync them:

```bash
(venv)$ pip-sync requirements.txt dev-requirements.txt
```

After that run the unit tests as described in the Unit Testing section to ensure that the updates do not cause incompatibilities in the project.

## Testing

### Test Setup

Automated testing is performed using [tox](https://tox.readthedocs.io/en/latest/index.html). Tox will automatically create virtual environments based on `tox.ini` for unit testing, PEP8 style guide checking, and documentation generation.

### Running Tests

Install tox (only needed once):

```bash
python3 -m pip install tox
```

Run all environments:

```bash
tox #To run a specific environment, specify it like: -e pep8
```

### Unit Testing

Unit testing is performed with [pytest](https://pytest.org/), a de facto standard Python unit testing framework. Some key advantages over the built-in [unittest](https://docs.python.org/3/library/unittest.html) module are:

1. Significantly less boilerplate needed for tests.
2. PEP8 compliant names (e.g. `pytest.raises()` instead of `self.assertRaises()`).
3. Vibrant ecosystem of plugins.

pytest will automatically discover and run tests by recursively searching for folders and `.py` files prefixed with `test`, as well as any functions prefixed by `test`.

The `tests` folder is created as a Python package (i.e., there is an `__init__.py` file within it) because this helps `pytest` uniquely namespace the test files. Without this, two test files cannot be named the same, even if they are in different sub-directories.

Code coverage is provided by the [pytest-cov](https://pytest-cov.readthedocs.io/en/latest/) plugin.

When running a unit test tox environment (e.g., `tox`, `tox -e py37`, etc.), a data file (e.g., `.coverage.py37`) containing the coverage data is generated. This file is not readable on its own, but when the `coverage` tox environment is run (e.g., `tox` or `tox -e coverage`), coverage from all unit test environments is combined into a single data file. An HTML report is generated in the `htmlcov` folder, showing each source file and indicating which lines were executed during unit testing. Open `htmlcov/index.html` in a web browser to view the report. Code coverage reports help identify areas of the project that are not currently tested.

Code coverage is configured in the `.coveragerc` file.

### Code Style Checking

[PEP8](https://www.python.org/dev/peps/pep-0008/) is the universally accepted style guide for Python code. PEP8 code compliance is verified using [flake8](http://flake8.pycqa.org/). flake8 is configured in the `[flake8]` section of `tox.ini`. Three extra flake8 plugins are also included:

- `pep8-naming`: Ensure functions, classes, and variables are named with correct casing.
- `flake8-quotes`: Ensure that `' '` style string quoting is used consistently.
- `flake8-import-order`: Ensure consistency in the way imports are grouped and sorted.

## Project Structure

### Traditional Layout

Traditionally, Python projects place the source for their packages in the root of the project structure:

```plaintext
root_folder
├── cryptosteganography
│   ├── __init__.py
│   ├── cli.py
│   └── lib.py
├── tests
│   ├── __init__.py
│   └── test_generate.py
├── tox.ini
└── setup.py
```

### Issues with the Traditional Layout

However, this structure is [known](https://docs.pytest.org/en/latest/goodpractices.html#tests-outside-application-code) to have bad interactions with `pytest` and `tox`, which are standard tools for maintaining Python projects. The fundamental issue is that tox creates an isolated virtual environment for testing. By installing the distribution into the virtual environment, `tox` ensures that the tests pass even after the distribution has been packaged and installed, thereby catching any errors in packaging and installation scripts, which are common.

Having the Python packages in the project root subverts this isolation for two reasons:

1. **Sys.path Issues with `pytest`**: Calling `python` in the project root (for example, `python -m pytest tests/`) [causes Python to add the current working directory](https://docs.pytest.org/en/latest/pythonpath.html#invoking-pytest-versus-python-m-pytest) (the project root) to `sys.path`, which Python uses to find modules. Because the source package `cryptosteganography` is in the project root, it shadows the `cryptosteganography` package installed in the tox environment.
2. **Namespace Collisions**: Calling `pytest` directly anywhere that it can find the tests will also add the project root to `sys.path` if the `tests` folder is a Python package (that is, it contains an `__init__.py` file). [pytest adds all folders containing packages](https://docs.pytest.org/en/latest/goodpractices.html#conventions-for-python-test-discovery) to `sys.path` because it imports the tests like regular Python modules.

### Recommended Project Structure

To properly test the project, the source packages must not be on the Python path. To prevent this, there are three possible solutions:

1. **Remove the `__init__.py` file from `tests` and run `pytest` directly as a tox command.**
2. **Remove the `__init__.py` file from `tests` and change the working directory of `python -m pytest` to `tests`.**
3. **Move the Source Packages to a Dedicated `src` Folder.**

The dedicated `src` directory is the [recommended solution](https://docs.pytest.org/en/latest/pythonpath.html#test-modules-conftest-py-files-inside-packages) by `pytest` when using tox. This solution is promoted because it is the least brittle, even though it deviates from the traditional Python project structure. It results in a directory structure like:

```plaintext
root_folder
├── src
│   └── cryptosteganography
│       ├── __init__.py
│       ├── cli.py
│       └── lib.py
├── tests
│   ├── __init__.py
│   ├── test_cli.py
│   └── test_lib.py
├── tox.ini
└── setup.py
```

### Benefits of the `src` Layout

- **Isolation**: Ensures that the source code is not accidentally imported from the project root, preserving the isolation of the virtual environment.
- **Packaging Accuracy**: Catches any errors in packaging and installation scripts early by installing the distribution into a controlled environment before testing.
- **Namespace Management**: Minimizes the risk of namespace collisions, making it easier to manage and discover tests.

Adopting the `src` layout is considered best practice for maintaining a clean and manageable project structure.

## Contribution Process

To contribute to cryptosteganography, follow these steps:

1. **Open an issue**: If you find a bug or have a request, open an issue first to discuss what you would like to change.
2. **Fork the repository**: Create your fork of the repository on GitHub.
3. **Create a feature branch**: Make your changes in a feature branch (`git checkout -b feature/FeatureName`).
4. **Testing and linting**: Run tests and ensure code style checks pass.
5. **Commit your changes**: Write clear and concise commit messages.
6. **Sync your branch**: Before pushing, make sure to pull the latest changes from the main branch and resolve any potential conflicts.
7. **Push the branch**: Push your branch to your forked repository (`git push origin feature/FeatureName`).
8. **Create a pull request**: Submit a pull request to merge your changes into the `main` branch.

We will review your pull request and provide feedback. Once approved, your changes will be merged. Thank you for your contributions!

## Issue and Pull Request Templates

We have set up templates to streamline the process of reporting issues and submitting pull requests. These templates ensure that you provide all the necessary information, making it easier for maintainers and contributors to collaborate effectively.

### Issue Templates

Our issue templates are located in the `.github/ISSUE_TEMPLATE` directory. When opening a new issue, you can choose from the following templates:

- **Bug Report:** Use this template to report bugs. It helps you provide all necessary information to reproduce and fix the bug. The template includes sections for describing the bug, steps to reproduce, expected behavior, screenshots, and environment details.
  
  - Template File: `.github/ISSUE_TEMPLATE/bug_report.md`

- **Feature Request:** Use this template to suggest new features or enhancements. It guides you in describing the problem, proposed solution, and any alternatives considered.
  
  - Template File: `.github/ISSUE_TEMPLATE/feature_request.md`

### Pull Request Template

When submitting a pull request, please use the provided template. This ensures that you include all relevant information about the changes you are proposing, the testing done, and the impact on the project. The template includes checkboxes for you to confirm that you have followed the contribution guidelines.

- Template File: `.github/PULL_REQUEST_TEMPLATE.md`
