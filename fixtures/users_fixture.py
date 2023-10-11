import pytest
from api.sendrequest_api.users_client import UsersClient


@pytest.fixture(scope="function", name="users")
def users_api_fixture() -> UsersClient:
    return UsersClient()
