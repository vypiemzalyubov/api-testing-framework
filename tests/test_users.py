import allure
import pytest
from http import HTTPStatus
from utils.asserts import Asserts
from utils.data.load_data import get_translation
from utils.models.users_model import UserList


pytest_plugins = ["fixtures.users_fixture"]
pytestmark = [allure.parent_suite("sendrequest"),
              allure.suite("users")]


class TestCompanies:

    @allure.title("Request data without parameters about the list of users")
    @pytest.mark.positive
    def test_get_user_list_without_parameters(self, users):
        response = users.users()
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(UserList)