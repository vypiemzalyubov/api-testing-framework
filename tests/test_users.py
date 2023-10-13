import allure
import pytest
from http import HTTPStatus
from utils.asserts import Asserts
from utils.data.load import get_translation
from utils.models.users_model import User, UserList


pytest_plugins = ["fixtures.users_fixture"]
pytestmark = [allure.parent_suite("sendrequest"),
              allure.suite("users")]


@pytest.mark.positive
class UsersPositive:

    @allure.title("Request data without parameters about the list of users")
    def test_get_user_list_without_parameters(self, users):
        response = users.get_users()
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(UserList)

    @allure.title("Request to check filtering of users by limit")
    @pytest.mark.parametrize("limit, total",
                             [(i, i) for i in range(7)])
    def test_get_user_list_by_limit(self, users, limit, total):
        params = {"limit": limit}
        response = users.get_users(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(UserList) \
            .has_sum_of_values("data", total)

    @allure.title("Request to check filtering of users by limit and offset")
    @pytest.mark.parametrize("limit, offset, user_id",
                             [(1, 4, 75), (1, 5, 76)])
    def test_get_user_list_by_limit_and_offset(self, users, limit, offset, user_id):
        params = {"limit": limit, "offset": offset}
        response = users.get_users(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(UserList) \
            .have_value_in_key("data[*].user_id", user_id)

    @allure.title("Request to check the creation of a user with a company")
    def test_create_user_with_company(self, users):
        payload = {"first_name": "vypiem1",
                   "last_name": "za_lyubov1", "company_id": 1}
        response = users.create_user(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.CREATED) \
            .validate_schema(User) \
            .have_value_in_key("first_name", "vypiem1") \
            .have_value_in_key("last_name", "za_lyubov1") \
            .have_value_in_key("company_id", 1)

    @allure.title("Request to check the creation of a user without a \"company_id\"")
    def test_create_user_without_company(self, users):
        payload = {"first_name": "vypiem2", "last_name": "za_lyubov2"}
        response = users.create_user(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.CREATED) \
            .validate_schema(User) \
            .have_value_in_key("first_name", "vypiem2") \
            .have_value_in_key("last_name", "za_lyubov2") \
            .have_value_in_key("company_id", None)

    @allure.title("Request to check the creation of a user without a \"first_name\"")
    def test_create_user_without_first_name(self, users):
        payload = {"last_name": "za_lyubov3"}
        response = users.create_user(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.CREATED) \
            .validate_schema(User) \
            .have_value_in_key("last_name", "za_lyubov3") \
            .have_value_in_key("first_name", None) \
            .have_value_in_key("company_id", None)


@pytest.mark.negative
class UsersNegative:

    @allure.title("Request to check filtering by limit equal to zero")
    def test_get_user_list_by_limit_where_limit_zero(self, users):
        params = {"limit": 0}
        response = users.get_users(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(UserList) \
            .has_sum_of_values("data", 0)

    @allure.title("Request to check filtering by offset greater than the total number of users")
    def test_get_user_list_by_offset_where_offset_greather_total(self, users):
        params = {"offset": 300000}
        response = users.get_users(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(UserList) \
            .has_sum_of_values("data", 0)

    @allure.title("Request to check the creation of a user without a required parameter \"last_name\"")
    def test_create_user_without_required_parameter_last_name(self, users):
        payload = {"first_name": "vypiem_test"}
        response = users.create_user(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNPROCESSABLE_ENTITY) \
            .have_value_in_key("detail[0].loc[0].body", "last_name") \
            .have_value_in_key("detail[0].msg", "field required")

    @allure.title("Request to check the creation of a user with an inactive company")
    @pytest.mark.parametrize(
        "company_id",
        [
            pytest.param(4, id="Nord BANKRUPT"),
            pytest.param(5, id="Apple CLOSED"),
            pytest.param(6, id="BitcoinCorp CLOSED"),
            pytest.param(7, id="Xiaomi BANKRUPT")
        ]
    )
    def test_create_user_with_inactive_company(self, users, company_id):
        payload = {"first_name": "vypiem_test",
                   "last_name": "za_lyubov_test", "company_id": company_id}
        response = users.create_user(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.BAD_REQUEST) \
            .have_value_in_key("detail.reason", f"User could not be assigned to company with id: {company_id}. Because it is not active")
