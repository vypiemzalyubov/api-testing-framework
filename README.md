# Api testing framework 

[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12-blue)](https://www.python.org/downloads/release/python-3120/)
[![License MIT](https://img.shields.io/badge/license-MIT-green)](https://github.com/vypiemzalyubov/api-testing-framework/blob/main/LICENSE)

It is a complete framework for automating API testing using **Python** and **Pytest**. This framework is used in the [**"Send Request"**](https://send-request.me/) API. 

CRUD methods (**GET**, **POST**, **PUT** and **DELETE**) are supported.

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

## :rocket: Getting Started
```bash
# Clone repository
git clone https://github.com/vypiemzalyubov/api-testing-framework.git

# Install virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

## :rocket: Running tests
```python
# Run all tests
pytest tests/

# Run positive test cases
pytest -m "positive"

# Run negative test cases
pytest -m "negative"
```
>Default startup options in `pytest.ini`:
>```python
>addopts = 
>        -s -v
>        --tb=short
>        --alluredir=allure-results
>```

## :rocket: Viewing reports
- Install [**Allure**](https://docs.qameta.io/allure/#_get_started) from the official website
- Generate Allure report
  
  ```bash
  allure serve
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
