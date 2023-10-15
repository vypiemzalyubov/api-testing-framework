import pytest
from api.sendrequest_api.auth_client import AuthClient


@pytest.fixture(scope="function", name="auth")
def auth_api_fixture() -> AuthClient:
    return AuthClient()