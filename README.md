# Api testing framework 

[![Python](https://img.shields.io/badge/python-3.11.2%2B-blue)](https://www.python.org/downloads/release/python-3112/)

This project implements a framework to automate testing of the [**"Send Request"**](https://send-request.me/) API

## :rocket: Description:

Automated CRUD (`POST`, `GET`, `PUT`, `DELETE`) APIs using `Python` and `Pytest`

## :rocket: Prerequisites:

[![Pytest](https://img.shields.io/badge/pytest-7.4.2-blue)](https://pypi.python.org/pypi/pytest)
[![HTTPX](https://img.shields.io/badge/httpx-0.25.0-blue)](https://pypi.org/project/httpx/)
[![Pydantic](https://img.shields.io/badge/pydantic-2.3.0-blue)](https://pypi.org/project/pydantic/)
[![Pydantic Settings](https://img.shields.io/badge/pydantic--settings-2.0.3-blue)](https://pypi.org/project/pydantic-settings/)
[![JSONPath](https://img.shields.io/badge/jsonpath--ng-1.6.0-blue)](https://pypi.org/project/jsonpath-ng/)
[![pytest-xdist](https://img.shields.io/badge/pytest--xdist-3.3.1-blue)](https://pypi.org/project/pytest-xdist/)
[![Allure Pytest](https://img.shields.io/badge/allure--pytest-2.13.2-blue)](https://pypi.python.org/pypi/allure-pytest)

## :rocket: Project Structure:

```
api-testing-framework/
├─ api
│  ├─ sendrequest_api/
│  |  ├─ auth_client.py
│  |  ├─ companies_client.py
│  |  ├─ issues_client.py
│  |  ├─ users_client.py
│  ├─ api_client.py
│  ├─ routes.py
├─ fixtures
│  ├─ auth_fixture.py
│  ├─ companies_fixture.py
│  ├─ issues_fixture.py
│  ├─ users_fixture.py
├─ tests/
│  ├─ __init__.py
│  ├─ test_auth.py
│  ├─ test_companies.py
│  ├─ test_issues.py
│  ├─ test_users.py
├─ utils
│  ├─ data/
│  |  ├─ load.py
│  ├─ models/
│  |  ├─ auth_model.py
│  |  ├─ companies_model.py
│  |  ├─ users_model.py
│  ├─ asserts.py
│  ├─ logger.py
│  ├─ parser.py
├─ .env
├─ .gitignore
├─ conftest.py
├─ docker-compose.yml
├─ Dockerfile
├─ pytest.ini
├─ README.md
├─ requirements.txt
├─ settings.py
```

## :rocket: Running in Docker

```bash
# Build an image named "api-testing-runner"
docker build -t api-testing-runner .

# Launch the container
docker run api-testing-runner

# Running with Docker Compose
docker-compose up --build
```
