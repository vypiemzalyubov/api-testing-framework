from http import HTTPStatus
import allure
import pytest
from utils.asserts import Asserts
from utils.models.companies_model import CompanyList


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
