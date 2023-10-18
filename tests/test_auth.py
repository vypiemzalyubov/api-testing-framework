import time
import allure
import pytest
from http import HTTPStatus
from utils.asserts import Asserts
from utils.data.load import load_data
from utils.models.auth_model import Token, UserAuth


pytestmark = [allure.feature("sendrequest"),
              allure.story("auth")]


@pytest.mark.positive
class AuthPositive:

    @allure.title("Request to receive authorization token and authorize the user")
    def test_get_auth_token_and_authorize_user(self, auth):
        # GETTING AUTH TOKEN
        payload = {"login": "John Malkovich",
                   "password": "qwerty12345", "timeout": 360}
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
            .validate_schema(UserAuth) \
            .have_value_in_key("user_name", "John Malkovich")

    @allure.title("Request to receive authorization token and authorize the user by checking the \"login\" boundary values")
    @pytest.mark.parametrize("login",
                             [("Mia"), ("Phil")])
    def test_get_auth_token_and_authorize_user_where_length_login_in_boundary_values(self, auth, login):
        # GETTING AUTH TOKEN
        payload = {"login": login, "password": "qwerty12345"}
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
            .validate_schema(UserAuth) \
            .have_value_in_key("user_name", login)


@pytest.mark.negative
class AuthNegative:

    @allure.title("Request to receive authorization token with invalid parameter \"password\"")
    def test_get_auth_token_with_invalid_password(self, auth):
        payload = {"login": "Ryan Gosling", "password": "test"}
        response = auth.create_auth_token(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.FORBIDDEN) \
            .have_value_in_key("detail.reason", "Invalid password")

    @allure.title("Request to receive authorization token without required parameter \"password\"")
    def test_get_auth_token_without_password(self, auth):
        payload = {"login": "Bill Skarsgård"}
        response = auth.create_auth_token(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNPROCESSABLE_ENTITY) \
            .have_value_in_key("detail[0].loc[0].body", "password") \
            .have_value_in_key("detail[0].msg", "field required")

    @allure.title("Request to receive authorization token with \"login\" shorter than three characters")
    def test_get_auth_token_where_login_less_three_chars(self, auth):
        payload = {"login": "ku", "password": "qwerty12345"}
        response = auth.create_auth_token(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNPROCESSABLE_ENTITY) \
            .have_value_in_key("detail[0].msg", "ensure this value has at least 3 characters")

    @allure.title("Request to receive authorization token without required parameter \"login\"")
    def test_get_auth_token_by_valid_password_and_without_login(self, auth):
        payload = {"password": "qwerty12345"}
        response = auth.create_auth_token(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNPROCESSABLE_ENTITY) \
            .have_value_in_key("detail[0].loc[0].body", "login") \
            .have_value_in_key("detail[0].msg", "field required")

    @allure.title("Request to receive authorization token with invalid parameter \"password\" and without required parameter \"login\"")
    def test_get_auth_token_by_invalid_password_and_without_login(self, auth):
        payload = {"password": "new_password"}
        response = auth.create_auth_token(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNPROCESSABLE_ENTITY) \
            .have_value_in_key("detail[0].loc[0].body", "login") \
            .have_value_in_key("detail[0].msg", "field required")

    @allure.title("Request to receive authorization token without parameters")
    def test_get_auth_token_without_parameters(self, auth):
        response = auth.create_auth_token()
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNPROCESSABLE_ENTITY) \
            .have_value_in_key("detail[0].msg", "field required")

    @allure.title("Request to retrieve user data without token")
    def test_authorize_user_without_token(self, auth):
        response = auth.auth_user()
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNAUTHORIZED) \
            .have_value_in_key("detail.reason", "Please use auth method for getting data for private method")

    @allure.title("Request to retrieve user data with invalid token")
    def test_authorize_user_with_invalid_token(self, auth):
        auth_header = {"x-token": "test_token"}
        response = auth.auth_user(auth_header)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.FORBIDDEN) \
            .have_value_in_key("detail.reason", "Token is incorrect. Please login and try again")

    @allure.title("Request to retrieve user data with expired token")
    def test_authorize_user_with_expired_token(self, auth):
        # GETTING AUTH TOKEN
        payload = {"login": "Laura Palmer",
                   "password": "qwerty12345", "timeout": 1}
        auth_response = auth.create_auth_token(payload)
        Asserts(auth_response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(Token)
        # GETTING TOKEN VALUE
        token = load_data.get_value(auth_response, "token")
        # WAITING FOR TOKEN TO EXPIRE
        time.sleep(2)
        # AUTHORIZATION USER
        auth_header = {"x-token": token}
        user_response = auth.auth_user(auth_header)
        Asserts(user_response) \
            .status_code_should_be(HTTPStatus.FORBIDDEN) \
            .have_value_in_key("detail.reason", "Token is expired. Please login and try again")
