import allure
import pytest
from http import HTTPStatus
from utils.asserts import Asserts
# from utils.data.load import load_data
# from utils.models.users_model import User, UserList


pytestmark = [allure.parent_suite("sendrequest"),
              allure.suite("issues")]


@pytest.mark.positive
class IssuesPositive:

    # @allure.title("Request data without parameters about the list of users")
    def test_issues(self, issues):
        pass
