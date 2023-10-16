import pytest
from api.sendrequest_api.issues_client import IssuesClient


@pytest.fixture(scope="function", name="issues")
def issues_api_fixture() -> IssuesClient:
    return IssuesClient()