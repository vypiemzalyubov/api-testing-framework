import allure
import pytest
from utils.asserts import Asserts
from utils.models.companies_schema import Company


pytest_plugins = ["fixtures.companies_api_fixture"]
pytestmark = [allure.parent_suite("sendrequest"),
              allure.suite("companies")]


class TestCompanies:

    @allure.title("Request to receive data on all companies")
    def test_get_all_companies(self, companies):
        response = companies.companies()
        Asserts(response) \
            .status_code_should_be(200) \
            .validate_schema(Company)

    @allure.title("Request with invalid arguments of the 'status' parameter")
    @pytest.mark.parametrize('status', ["active", "bankrupt", "closed", "test"])
    def test_get_companies_with_invalid_status(self, companies, status):
        params = {"status": status}
        response = companies.companies(params)
        Asserts(response) \
            .status_code_should_be(422) \
            .have_value_in_key("msg", "value is not a valid enumeration member; permitted: 'ACTIVE', 'BANKRUPT', 'CLOSED'")
