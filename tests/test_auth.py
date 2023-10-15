import allure
import pytest
from http import HTTPStatus
from utils.asserts import Asserts
from utils.data.load import load_data
from utils.models.auth_model import Token, AuthUser


pytest_plugins = ["fixtures.auth_fixture"]
pytestmark = [allure.parent_suite("sendrequest"),
              allure.suite("auth")]


@pytest.mark.positive
class AuthPositive:

    @allure.title("Request to receive an authorization token and authorize the user")
    def test_get_auth_token_and_authorize_user(self, auth):
        # GETTING AUTH TOKEN
        payload = {"login": "John Malkovich", "password": "qwerty12345", "timeout": 360}
        auth_response = auth.create_auth_token(payload)
        Asserts(auth_response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(Token)
        # GETTING TOKEN VALUE
        token = load_data.get_value(auth_response, "token")
        # AUTHORIZATION USER
        auth_header = {"x-token": token}
        user_response = auth.auth_user(auth_header)
        Asserts(user_response) \
            .status_code_should_be(HTTPStatus.OK) \
            .have_value_in_key("user_name", "John Malkovich")
        