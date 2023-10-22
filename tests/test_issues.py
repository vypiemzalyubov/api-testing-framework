from http import HTTPStatus
import allure
import pytest
from utils.asserts import Asserts
from utils.data.load import load_data
from utils.models.companies_model import Company, CompanyList


pytestmark = [allure.feature("Send Request"),
              allure.story("issues")]


@pytest.mark.positive
class IssuesPositive:

    @allure.title("Get the list of issues companies without query parameters")
    def test_issues_get_company_list_without_parameters(self, issues):
        response = issues.get_issues_companies()
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(CompanyList)

    @allure.title("Get list of issues companies filtered by status")
    @pytest.mark.parametrize(
        "status, company_status",
        [
            pytest.param("ACTIVE", "ACTIVE", marks=pytest.mark.xfail(
                reason="The CLOSED filter is permanently applied regardless of the value passed in")),
            pytest.param("BANKRUPT", "BANKRUPT", marks=pytest.mark.xfail(
                reason="The CLOSED filter is permanently applied regardless of the value passed in")),
            pytest.param("CLOSED", "CLOSED")
        ]
    )
    def test_issues_get_company_list_by_status(self, issues, status, company_status):
        params = {"status": status}
        response = issues.get_issues_companies(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(CompanyList) \
            .have_value_in_key("data[*].company_status", company_status)

    @allure.title("Get list of issues companies filtered by limit")
    @pytest.mark.parametrize(
        "limit, total",
        [
            pytest.param(0, 0),
            pytest.param(1, 1),
            pytest.param(2, 2),
            pytest.param(3, 3, marks=pytest.mark.xfail(
                reason="There are no companies with \"ACTIVE\" and \"BANKRUPT\" statuses")),
            pytest.param(6, 6, marks=pytest.mark.xfail(
                reason="There are no companies with \"ACTIVE\" and \"BANKRUPT\" statuses"))
        ]
    )
    def test_issues_get_company_list_by_limit(self, issues, limit, total):
        params = {"limit": limit}
        response = issues.get_issues_companies(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(CompanyList) \
            .has_sum_of_values("data", total)

    @allure.title("Get list of issues companies filtered by limit and offset")
    @pytest.mark.parametrize("limit, offset, company_id",
                             [(1, 0, 5), (1, 1, 6)])
    def test_issues_get_company_list_by_limit_and_offset(self, issues, limit, offset, company_id):
        params = {"limit": limit, "offset": offset}
        response = issues.get_issues_companies(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(CompanyList) \
            .have_value_in_key("data[*].company_id", company_id)

    @allure.title("Get issues company data by id with waiting for a long server response")
    @pytest.mark.parametrize(
        "company_id, response_id, response_name, response_status",
        [
            pytest.param(1, 1, "Tesla", "ACTIVE",
                         id="Tesla - long server response"),
            pytest.param(4, 4, "Nord", "BANKRUPT",
                         id="Nord - long server response"),
            pytest.param(6, 6, "BitcoinCorp", "CLOSED",
                         id="BitcoinCorp - long server response")
        ]
    )
    def test_issues_get_company_by_id(self, issues, company_id, response_id, response_name, response_status):
        response = issues.get_issues_company(company_id)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(Company) \
            .have_value_in_key("data[*].company_id", response_id) \
            .have_value_in_key("data[*].company_name", response_name) \
            .have_value_in_key("data[*].company_status", response_status)

    @allure.title("Get issues company data by id and available localization with waiting for a long server response")
    @pytest.mark.parametrize(
        "company_id, headers, response_translation",
        [
            pytest.param(3, {"Accept-Language": "RU"},
                         load_data.load_translation("RU"), id="translation RU - long server response"),
            pytest.param(1, {"Accept-Language": "EN"},
                         load_data.load_translation("EN"), id="translation EN - long server response"),
            pytest.param(1, {"Accept-Language": "PL"},
                         load_data.load_translation("PL"), id="translation PL - long server response")
        ]
    )
    def test_issues_get_company_by_id_and_localization(self, issues, company_id, headers, response_translation):
        response = issues.get_issues_company(company_id, headers)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(Company) \
            .have_value_in_key("description", response_translation)


@pytest.mark.negative
class IssuesNegative:

    @allure.title("Get the list of issues companies with invalid query parameter status")
    @pytest.mark.parametrize("status",
                             ["active", "bankrupt", "closed", "test"])
    def test_issues_get_company_list_by_invalid_status(self, issues, status):
        params = {"status": status}
        response = issues.get_issues_companies(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNPROCESSABLE_ENTITY) \
            .have_value_in_key("detail[0].msg", "value is not a valid enumeration member; permitted: 'ACTIVE', 'BANKRUPT', 'CLOSED'")

    @allure.title("Request to check filtering by a limit greater than the total number of issues companies")
    def test_issues_get_company_list_by_limit_where_limit_greather_total(self, issues):
        params = {"limit": 8}
        response = issues.get_issues_companies(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .has_sum_of_values("data", 2)

    @allure.title("Request to check filtering by offset greater than or equal to the total number of issues companies")
    @pytest.mark.parametrize("offset, total",
                             [(2, 0), (3, 0)])
    def test_issues_get_company_list_by_offset_where_offset_greather_or_equal_total(self, issues, offset, total):
        params = {"offset": offset}
        response = issues.get_issues_companies(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .has_sum_of_values("data", total)

    @allure.title("Request for data by id on non-existent issues company with waiting for a long server response")
    def test_issues_get_non_existent_company_by_id(self, issues):
        response = issues.get_issues_company(9)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.NOT_FOUND) \
            .have_value_in_key("detail.reason", "Company with requested id: 9 is absent")

    @allure.title("Request issues company data by id and unavailable localization with waiting for a long server response")
    @pytest.mark.parametrize(
        "company_id, headers, response_locale",
        [
            pytest.param(1, {"Accept-Language": "DE"}, "DE",
                         id="DE - long server response"),
            pytest.param(5, {"Accept-Language": "US"}, "US",
                         id="US - long server response"),
            pytest.param(3, {"Accept-Language": "NO"}, "NO",
                         id="NO - long server response")
        ]
    )
    def test_issues_get_company_by_id_and_unavailable_localization(self, issues, company_id, headers, response_locale):
        response = issues.get_issues_company(company_id, headers)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(Company) \
            .have_value_not_in_key("description_lang[*].translation_lang", response_locale)
