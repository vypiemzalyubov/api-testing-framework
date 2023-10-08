# Api testing framework 

[![Python](https://img.shields.io/badge/python-3.11.2%2B-blue)](https://www.python.org/downloads/release/python-3112/)

This project implements a framework to automate testing of the [**"Send Request"**](https://send-request.me/) API using `Python` and `Pytest`

## Prerequisites:

[![Pytest](https://img.shields.io/badge/pytest-7.4.2-blue)](https://pypi.python.org/pypi/pytest)
[![HTTPX](https://img.shields.io/badge/httpx-0.25.0-blue)](https://pypi.org/project/httpx/)
[![Pydantic](https://img.shields.io/badge/pydantic-2.3.0-blue)](https://pypi.org/project/pydantic/)
[![JSONPath](https://img.shields.io/badge/jsonpath--ng-1.6.0-blue)](https://pypi.org/project/jsonpath-ng/)
[![python-dotenv](https://img.shields.io/badge/python--dotenv-1.0.0-blue)](https://pypi.org/project/python-dotenv/)
[![pytest-xdist](https://img.shields.io/badge/pytest--xdist-3.3.1-blue)](https://pypi.org/project/pytest-xdist/)
[![Allure Pytest](https://img.shields.io/badge/allure--pytest-2.13.2-blue)](https://pypi.python.org/pypi/allure-pytest)

## Project Structure:

```
api-testing-framework/
├─ api
│  ├─ sendrequest_api/
│  |  ├─ companies_api.py
│  ├─ api_client.py
├─ fixtures
│  ├─ companies_api_fixture.py
├─ tests/
│  ├─ __init__.py
│  ├─ test_companies.py
├─ utils
│  ├─ models/
│  |  ├─ companies_model.py
│  ├─ asserts.py
│  ├─ logger.py
│  ├─ parser.py
├─ .gitignore
├─ README.md
├─ pytest.ini
├─ requirements.txt
```
