import allure
import pytest
from utils.asserts import Asserts
from utils.models.companies_schema import Company


pytest_plugins = ["fixtures.companies_api_fixture"]
pytestmark = [allure.parent_suite("sendrequest"),
              allure.suite("companies")]


class TestCompanies:

    @allure.title("Request for data on companies without parameters")
    @pytest.mark.positive
    def test_get_companies_without_parameters(self, companies):
        response = companies.companies()
        Asserts(response) \
            .status_code_should_be(200) \
            .validate_schema(Company)

    @allure.title("Request to check filtering by status")
    @pytest.mark.positive
    @pytest.mark.parametrize("status, company_status",
                             [("ACTIVE", "ACTIVE"), ("BANKRUPT", "BANKRUPT"), ("CLOSED", "CLOSED")])
    def test_get_companies_by_status(self, companies, status, company_status):
        params = {"status": status}
        response = companies.companies(params)
        Asserts(response) \
            .status_code_should_be(200) \
            .validate_schema(Company) \
            .have_value_in_key("data[*].company_status", company_status)

    @allure.title("Request to check filtering by limit")
    @pytest.mark.positive
    @pytest.mark.parametrize("limit, total",
                             [(i, i) for i in range(7)])
    def test_get_companies_by_limit(self, companies, limit, total):
        params = {"limit": limit}
        response = companies.companies(params)
        Asserts(response) \
            .status_code_should_be(200) \
            .validate_schema(Company) \
            .have_sum_of_value("data", total)

    @allure.title("Request with invalid arguments of the \"status\" parameter")
    @pytest.mark.negative
    @pytest.mark.parametrize("status",
                             ["active", "bankrupt", "closed", "test"])
    def test_get_companies_by_invalid_status(self, companies, status):
        params = {"status": status}
        response = companies.companies(params)
        Asserts(response) \
            .status_code_should_be(422) \
            .have_value_in_key("detail[0].msg", "value is not a valid enumeration member; permitted: 'ACTIVE', 'BANKRUPT', 'CLOSED'")

    @allure.title("Request to check filtering by a limit greater than the total number of companies")
    @pytest.mark.negative
    def test_get_companies_by_limit_where_limit_greather_total(self, companies):
        params = {"limit": 8}
        response = companies.companies(params)
        Asserts(response) \
            .status_code_should_be(200) \
            .have_sum_of_value("data", 7)
        
    @allure.title("Request to check filtering by offset greater than or equal to the total number of companies")
    @pytest.mark.negative
    @pytest.mark.parametrize("offset, total",
                             [(7, 0), (8, 0)])    
    def test_get_companies_by_offset_where_offset_greather_or_equal_total(self, companies, offset, total):
        params = {"offset": offset}
        response = companies.companies(params)
        Asserts(response) \
            .status_code_should_be(200) \
            .have_sum_of_value("data", total)        