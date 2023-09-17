import allure
import pytest
from utils.asserts import Asserts
from utils.models.companies_schema import Company


pytest_plugins = ["fixtures.companies_api_fixture"]


class TestCompanies:

    @allure.title('Request to receive data on all companies')
    def test_get_all_companies(self, companies_api_fixture):
        response = companies_api_fixture.companies()
        Asserts.status_code_should_be(response, 200)
        Asserts.validate_response(response, Company)
