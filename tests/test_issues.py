from http import HTTPStatus
import allure
import pytest
from utils.asserts import Asserts
from utils.data.load import load_data
from utils.models.companies_model import Company, CompanyList
from utils.models.users_model import User


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

    @allure.title("Request to check issues user data by id")
    @pytest.mark.parametrize(
        "user_id, company_id",
        [
            pytest.param(29175, None, marks=pytest.mark.xfail(
                reason="\"user_id\" and \"company_id\" fields are missing in the response")),
            pytest.param(97, 3, marks=pytest.mark.xfail(
                reason="\"user_id\" and \"company_id\" fields are missing in the response")),
            pytest.param(101, 1, marks=pytest.mark.xfail(
                reason="\"user_id\" and \"company_id\" fields are missing in the response"))
        ]
    )
    def test_issues_get_user_by_id(self, issues, user_id, company_id):
        response = issues.get_issues_user(user_id)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.ACCEPTED) \
            .validate_schema(User) \
            .have_value_in_key("user_id", user_id) \
            .have_value_in_key("company_id", company_id)

    @allure.title("Request to check the creation of a issues user with a company")
    @pytest.mark.xfail(reason="The user is created with incorrect data")
    def test_issues_create_user_with_company_id(self, issues):
        payload = {"first_name": "Dennis",
                   "last_name": "Ritchie", "company_id": 1}
        response = issues.create_issues_user(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.CREATED) \
            .validate_schema(User) \
            .have_value_in_key("first_name", "Dennis") \
            .have_value_in_key("last_name", "Ritchie") \
            .have_value_in_key("company_id", 1)

    @allure.title("Request to check the creation of a issues user without a \"company_id\"")
    @pytest.mark.xfail(reason="The user is created with incorrect data")
    def test_issues_create_user_without_company_id(self, issues):
        payload = {"first_name": "Tim", "last_name": "Berners-Lee"}
        response = issues.create_issues_user(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.CREATED) \
            .validate_schema(User) \
            .have_value_in_key("first_name", "Tim") \
            .have_value_in_key("last_name", "Berners-Lee") \
            .have_value_in_key("company_id", None)

    @allure.title("Request to check the creation of a issues user without a \"first_name\"")
    @pytest.mark.xfail(reason="The user is created with incorrect data")
    def test_issues_create_user_without_first_name(self, issues):
        payload = {"last_name": "Stroustrup", "company_id": 2}
        response = issues.create_issues_user(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.CREATED) \
            .validate_schema(User) \
            .have_value_in_key("last_name", "Stroustrup") \
            .have_value_in_key("company_id", 2) \
            .have_value_in_key("first_name", None)

    @allure.title("Request to check the creation of a issues user without a \"first_name\" and \"company_id\"")
    @pytest.mark.xfail(reason="The user is created with incorrect data")
    def test_issues_create_user_without_first_name_and_company_id(self, issues):
        payload = {"last_name": "Torvalds"}
        response = issues.create_issues_user(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.CREATED) \
            .validate_schema(User) \
            .have_value_in_key("last_name", "Torvalds") \
            .have_value_in_key("first_name", None) \
            .have_value_in_key("company_id", None)

    @allure.title("Request to check issues user creation and retrieve the created issues user")
    @pytest.mark.xfail(reason="The user is created with incorrect data")
    def test_issues_creation_and_getting_created_user(self, issues):
        # CREATING USER
        payload = {"first_name": "Billy", "last_name": "Milligan"}
        user_creation = issues.create_issues_user(payload)
        Asserts(user_creation) \
            .status_code_should_be(HTTPStatus.CREATED) \
            .validate_schema(User) \
            .have_value_in_key("first_name", "Billy") \
            .have_value_in_key("last_name", "Milligan")
        # GETTING USER_ID
        user_id = load_data.get_value(user_creation, "user_id")
        # GETTING USER
        user_getting = issues.get_issues_user(user_id)
        Asserts(user_getting) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(User) \
            .have_value_in_key("first_name", "Billy") \
            .have_value_in_key("last_name", "Milligan") \
            .have_value_in_key("company_id", None)


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

    @allure.title("Request to check issues user by invalid \"user_id\"")
    @pytest.mark.parametrize("user_id",
                             [(-1), (0), (999999)])
    def test_issues_get_user_by_invalid_user_id(self, issues, user_id):
        response = issues.get_issues_user(user_id)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.NOT_FOUND) \
            .have_value_in_key("detail.reason", f"User with requested id: {user_id} is absent")

    @allure.title("Request to check the getting of a issues user without a required parameter \"user_id\"")
    def test_issues_get_user_without_user_id(self, issues):
        response = issues.get_issues_user()
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNPROCESSABLE_ENTITY) \
            .have_value_in_key("detail[0].loc[1]", "user_id") \
            .have_value_in_key("detail[0].msg", "value is not a valid integer")

    @allure.title("Request to check the creation of a issues user without a required parameter \"last_name\"")
    def test_issues_create_user_without_required_parameter_last_name(self, issues):
        payload = {"first_name": "Kanye"}
        response = issues.create_issues_user(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNPROCESSABLE_ENTITY) \
            .have_value_in_key("detail[0].loc[0].body", "last_name") \
            .have_value_in_key("detail[0].msg", "field required")

    @allure.title("Request to check the creation of a issues user with an inactive company")
    @pytest.mark.parametrize(
        "company_id",
        [
            pytest.param(4, id="Nord BANKRUPT", marks=pytest.mark.xfail(
                reason="A user is created with a binding to an inactive company")),
            pytest.param(5, id="Apple CLOSED", marks=pytest.mark.xfail(
                reason="A user is created with a binding to an inactive company")),
            pytest.param(6, id="BitcoinCorp CLOSED", marks=pytest.mark.xfail(
                reason="A user is created with a binding to an inactive company")),
            pytest.param(7, id="Xiaomi BANKRUPT", marks=pytest.mark.xfail(
                reason="A user is created with a binding to an inactive company"))
        ]
    )
    def test_issues_create_user_with_inactive_company(self, issues, company_id):
        payload = {"first_name": "James",
                   "last_name": "Gosling", "company_id": company_id}
        response = issues.create_issues_user(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.BAD_REQUEST) \
            .have_value_in_key("detail.reason", f"User could not be assigned to company with id: {company_id}. Because it is not active")
