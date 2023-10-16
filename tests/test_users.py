import allure
import pytest
from http import HTTPStatus
from utils.asserts import Asserts
from utils.data.load import load_data
from utils.models.users_model import User, UserList


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
    def test_create_user_with_company_id(self, users):
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
    def test_create_user_without_company_id(self, users):
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
        payload = {"last_name": "za_lyubov3", "company_id": 2}
        response = users.create_user(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.CREATED) \
            .validate_schema(User) \
            .have_value_in_key("last_name", "za_lyubov3") \
            .have_value_in_key("company_id", 2) \
            .have_value_in_key("first_name", None)

    @allure.title("Request to check the creation of a user without a \"first_name\" and \"company_id\"")
    def test_create_user_without_first_name_and_company_id(self, users):
        payload = {"last_name": "za_lyubov4"}
        response = users.create_user(payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.CREATED) \
            .validate_schema(User) \
            .have_value_in_key("last_name", "za_lyubov4") \
            .have_value_in_key("first_name", None) \
            .have_value_in_key("company_id", None)

    @allure.title("Request to check user data by id")
    @pytest.mark.parametrize(
        "user_id, first_name, last_name, company_id",
        [
            (29175, None, "za_lyubov4", None),
            (97, "vlad", "vlad", 3),
            (101, "Ne ny eto odnoznachno", "BAGGGGGGGG", 1)
        ]
    )
    def test_get_user_by_id(self, users, user_id, first_name, last_name, company_id):
        response = users.get_user(user_id)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(User) \
            .have_value_in_key("first_name", first_name) \
            .have_value_in_key("last_name", last_name) \
            .have_value_in_key("company_id", company_id)

    @allure.title("Request to check user creation and retrieve the created user")
    def test_creation_and_getting_created_user(self, users):
        # CREATING USER
        payload = {"first_name": "Roque", "last_name": "Santa Cruz"}
        user_creation = users.create_user(payload)
        Asserts(user_creation) \
            .status_code_should_be(HTTPStatus.CREATED) \
            .validate_schema(User) \
            .have_value_in_key("first_name", "Roque") \
            .have_value_in_key("last_name", "Santa Cruz")
        # GETTING USER_ID
        user_id = load_data.get_value(user_creation, "user_id")
        # GETTING USER
        user_getting = users.get_user(user_id)
        Asserts(user_getting) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(User) \
            .have_value_in_key("first_name", "Roque") \
            .have_value_in_key("last_name", "Santa Cruz") \
            .have_value_in_key("company_id", None)

    @allure.title("Request to check \"first_name\" and \"last_name\" updating of existing user")
    def test_update_first_name_and_last_name_of_existing_user(self, users):
        payload = {"first_name": "new_name", "last_name": "new_surname"}
        response = users.update_user(96, payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(User) \
            .have_value_in_key("first_name", "new_name") \
            .have_value_in_key("last_name", "new_surname")

    @allure.title("Request to check \"last_name\" and \"company_id\" updating of existing user")
    def test_update_last_name_and_company_id_of_existing_user(self, users):
        payload = {"last_name": "Marshall", "company_id": 1}
        response = users.update_user(68, payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(User) \
            .have_value_in_key("last_name", "Marshall") \
            .have_value_in_key("company_id", 1)

    @allure.title("Request to check user creation, updating and retrieve the updated user")
    def test_creation_updating_and_getting_updated_user(self, users):
        # CREATING USER
        payload = {"first_name": "Alan",
                   "last_name": "Turing", "company_id": 1}
        user_creation = users.create_user(payload)
        Asserts(user_creation) \
            .status_code_should_be(HTTPStatus.CREATED) \
            .validate_schema(User) \
            .have_value_in_key("first_name", "Alan") \
            .have_value_in_key("last_name", "Turing") \
            .have_value_in_key("company_id", 1)
        # GETTING USER_ID
        user_id = load_data.get_value(user_creation, "user_id")
        # UPDATING USER
        payload = {"first_name": "Stephen",
                   "last_name": "Hawking", "company_id": 2}
        user_updating = users.update_user(user_id, payload)
        Asserts(user_updating) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(User) \
            .have_value_in_key("first_name", "Stephen") \
            .have_value_in_key("last_name", "Hawking") \
            .have_value_in_key("company_id", 2)
        # GETTING USER
        user_getting = users.get_user(user_id)
        Asserts(user_getting) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(User) \
            .have_value_in_key("first_name", "Stephen") \
            .have_value_in_key("last_name", "Hawking") \
            .have_value_in_key("company_id", 2)

    @allure.title("Request to check deletion of a created user")
    def test_delete_of_created_user(self, users):
        # CREATING USER
        payload = {"first_name": "Jimi", "last_name": "Hendrix"}
        user_creation = users.create_user(payload)
        Asserts(user_creation) \
            .status_code_should_be(HTTPStatus.CREATED) \
            .validate_schema(User) \
            .have_value_in_key("first_name", "Jimi") \
            .have_value_in_key("last_name", "Hendrix") \
            # GETTING USER_ID
        user_id = load_data.get_value(user_creation, "user_id")
        # DELETED USER
        user_deletion = users.delete_user(user_id)
        Asserts(user_deletion) \
            .status_code_should_be(HTTPStatus.ACCEPTED)
        # GETTING DELETED USER
        user_getting = users.get_user(user_id)
        Asserts(user_getting) \
            .status_code_should_be(HTTPStatus.NOT_FOUND) \
            .have_value_in_key("detail.reason", f"User with requested id: {user_id} is absent")


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

    @allure.title("Request to check user by invalid \"user_id\"")
    @pytest.mark.parametrize("user_id",
                             [(-1), (0), (999999)])
    def test_get_user_by_invalid_user_id(self, users, user_id):
        response = users.get_user(user_id)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.NOT_FOUND) \
            .have_value_in_key("detail.reason", f"User with requested id: {user_id} is absent")

    @allure.title("Request to check the getting of a user without a required parameter \"user_id\"")
    def test_get_user_without_user_id(self, users):
        response = users.get_user()
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNPROCESSABLE_ENTITY) \
            .have_value_in_key("detail[0].loc[1]", "user_id") \
            .have_value_in_key("detail[0].msg", "value is not a valid integer")

    @allure.title("Request to check if the \"first_name\" field of an existing user has been updated without the mandatory \"last_name\" parameter")
    def test_update_existing_user_without_required_parameter_last_name(self, users):
        payload = {"first_name": "new_surname7"}
        response = users.update_user(68, payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNPROCESSABLE_ENTITY) \
            .have_value_in_key("detail[0].loc[0].body", "last_name") \
            .have_value_in_key("detail[0].msg", "field required")

    @allure.title("Request to check update of a non-existent user")
    @pytest.mark.parametrize("user_id, last_name",
                             [(-1, "surname1"), (0, "surname2"), (888888, "surname3")])
    def test_update_non_existent_user(self, users, user_id, last_name):
        payload = {"last_name": last_name}
        response = users.update_user(user_id, payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.NOT_FOUND) \
            .have_value_in_key("detail.reason", f"User with requested id: {user_id} is absent")

    @allure.title("Request to check if the user's \"company_id\" is updated to an inactive company")
    @pytest.mark.parametrize(
        "user_id, last_name, company_id",
        [
            pytest.param(96, "Babel", 4, id="Nord BANKRUPT"),
            pytest.param(97, "Keane", 5, id="Apple CLOSED"),
            pytest.param(98, "Murphy", 6, id="BitcoinCorp CLOSED"),
            pytest.param(99, "Tucker", 7, id="Xiaomi BANKRUPT")
        ]
    )
    def test_update_last_name_and_company_id_user_where_company_inactive(self, users, user_id, last_name, company_id):
        payload = {"last_name": last_name, "company_id": company_id}
        response = users.update_user(user_id, payload)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.BAD_REQUEST) \
            .have_value_in_key("detail.reason", f"User could not be assigned to company with id: {company_id}. Because it is not active")

    @allure.title("Request to check delete of a non-existent user")
    @pytest.mark.parametrize("user_id",
                             [(-1), (0), (777777)])
    def test_delete_of_non_existent_user(self, users, user_id):
        response = users.get_user(user_id)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.NOT_FOUND) \
            .have_value_in_key("detail.reason", f"User with requested id: {user_id} is absent")

    @allure.title("Request to check the deleting of a user without a required parameter \"user_id\"")
    def test_delete_user_without_required_parameter_user_id(self, users):
        response = users.get_user()
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNPROCESSABLE_ENTITY) \
            .have_value_in_key("detail[0].loc[1]", "user_id") \
            .have_value_in_key("detail[0].msg", "value is not a valid integer")
