import pytest
from api.sendrequest_api.companies_client import CompaniesClient


@pytest.fixture(scope="function", name="companies")
def companies_api_fixture() -> CompaniesClient:
    return CompaniesClient()
