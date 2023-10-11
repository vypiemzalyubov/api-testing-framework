import pytest
from api.sendrequest_api.users_api import UsersApi


@pytest.fixture(scope="function", name="users")
def users_api_fixture() -> UsersApi:
    return UsersApi()
