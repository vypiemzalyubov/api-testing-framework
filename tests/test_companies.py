import allure
import pytest
from http import HTTPStatus
from utils.asserts import Asserts
from utils.data.load import load_data
from utils.models.companies_model import Company, CompanyList


pytestmark = [allure.parent_suite("sendrequest"),
              allure.suite("companies")]


@pytest.mark.positive
class CompaniesPositive:

    @allure.title("Request data without parameters about the list of companies")
    def test_get_company_list_without_parameters(self, companies):
        response = companies.get_companies()
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(CompanyList)

    @allure.title("Request to check filtering by status")
    @pytest.mark.parametrize("status, company_status",
                             [("ACTIVE", "ACTIVE"), ("BANKRUPT", "BANKRUPT"), ("CLOSED", "CLOSED")])
    def test_get_company_list_by_status(self, companies, status, company_status):
        params = {"status": status}
        response = companies.get_companies(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(CompanyList) \
            .have_value_in_key("data[*].company_status", company_status)

    @allure.title("Request to check filtering of companies by limit")
    @pytest.mark.parametrize("limit, total",
                             [(i, i) for i in range(7)])
    def test_get_company_list_by_limit(self, companies, limit, total):
        params = {"limit": limit}
        response = companies.get_companies(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(CompanyList) \
            .has_sum_of_values("data", total)

    @allure.title("Request to check filtering of companies by limit and offset")
    @pytest.mark.parametrize("limit, offset, company_id",
                             [(1, 4, 5), (1, 5, 6)])
    def test_get_company_list_by_limit_and_offset(self, companies, limit, offset, company_id):
        params = {"limit": limit, "offset": offset}
        response = companies.get_companies(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(CompanyList) \
            .have_value_in_key("data[*].company_id", company_id)

    @allure.title("Request company data by id")
    @pytest.mark.parametrize(
        "company_id, response_id, response_name, response_status",
        [
            (1, 1, "Tesla", "ACTIVE"),
            (4, 4, "Nord", "BANKRUPT"),
            (6, 6, "BitcoinCorp", "CLOSED")
        ]
    )
    def test_get_company_by_id(self, companies, company_id, response_id, response_name, response_status):
        response = companies.get_company(company_id)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(Company) \
            .have_value_in_key("data[*].company_id", response_id) \
            .have_value_in_key("data[*].company_name", response_name) \
            .have_value_in_key("data[*].company_status", response_status)

    @allure.title("Request company data by id and available localization")
    @pytest.mark.parametrize(
        "company_id, headers, response_translation",
        [
            pytest.param(3, {"Accept-Language": "RU"},
                         load_data.load_translation("RU"), id="translation RU"),
            pytest.param(1, {"Accept-Language": "EN"},
                         load_data.load_translation("EN"), id="translation EN"),
            pytest.param(1, {"Accept-Language": "PL"},
                         load_data.load_translation("PL"), id="translation PL")
        ]
    )
    def test_get_company_by_id_and_localization(self, companies, company_id, headers, response_translation):
        response = companies.get_company(company_id, headers)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(Company) \
            .have_value_in_key("description", response_translation)


@pytest.mark.negative
class CompaniesNegative:

    @allure.title("Request with invalid arguments of the \"status\" parameter")
    @pytest.mark.parametrize("status",
                             ["active", "bankrupt", "closed", "test"])
    def test_get_company_list_by_invalid_status(self, companies, status):
        params = {"status": status}
        response = companies.get_companies(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNPROCESSABLE_ENTITY) \
            .have_value_in_key("detail[0].msg", "value is not a valid enumeration member; permitted: 'ACTIVE', 'BANKRUPT', 'CLOSED'")

    @allure.title("Request to check filtering by a limit greater than the total number of companies")
    def test_get_company_list_by_limit_where_limit_greather_total(self, companies):
        params = {"limit": 8}
        response = companies.get_companies(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .has_sum_of_values("data", 7)

    @allure.title("Request to check filtering by offset greater than or equal to the total number of companies")
    @pytest.mark.parametrize("offset, total",
                             [(7, 0), (8, 0)])
    def test_get_company_list_by_offset_where_offset_greather_or_equal_total(self, companies, offset, total):
        params = {"offset": offset}
        response = companies.get_companies(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .has_sum_of_values("data", total)

    @allure.title("Request for data by id on non-existent company")
    def test_get_non_existent_company_by_id(self, companies):
        response = companies.get_company(10)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.NOT_FOUND) \
            .have_value_in_key("detail.reason", "Company with requested id: 10 is absent")

    @allure.title("Request company data by id and unavailable localization")
    @pytest.mark.parametrize(
        "company_id, headers, response_locale",
        [
            (1, {"Accept-Language": "AR"}, "AR"),
            (5, {"Accept-Language": "RU"}, "RU"),
            (3, {"Accept-Language": "ES"}, "ES")
        ]
    )
    def test_get_company_by_id_and_unavailable_localization(self, companies, company_id, headers, response_locale):
        response = companies.get_company(company_id, headers)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(Company) \
            .have_value_not_in_key("description_lang[*].translation_lang", response_locale)
