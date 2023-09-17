import pytest
from api.companies_api import CompaniesApi


@pytest.fixture(scope="function")
def companies_api_fixture() -> CompaniesApi:
    return CompaniesApi()