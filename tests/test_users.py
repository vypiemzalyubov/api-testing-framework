import allure
import pytest
from http import HTTPStatus
from utils.asserts import Asserts
from utils.data.load_data import get_translation
from utils.models.users_model import UserList


pytest_plugins = ["fixtures.users_fixture"]
pytestmark = [allure.parent_suite("sendrequest"),
              allure.suite("users")]


@pytest.mark.positive
class TestUsersPositive:

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