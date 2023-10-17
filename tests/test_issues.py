import allure
import pytest
from http import HTTPStatus
from utils.asserts import Asserts
from utils.models.companies_model import Company, CompanyList
# from utils.data.load import load_data
# from utils.models.users_model import User, UserList


pytestmark = [allure.parent_suite("sendrequest"),
              allure.suite("issues")]


@pytest.mark.positive
class IssuesPositive:

    @allure.title("Request issues data without parameters about the list of companies")
    def test_issues_get_company_list_without_parameters(self, issues):
        response = issues.get_issues_companies()
        Asserts(response) \
            .status_code_should_be(HTTPStatus.OK) \
            .validate_schema(CompanyList)
        

@pytest.mark.negative
class IssuesNegative:

    @allure.title("Request with invalid arguments of the \"status\" parameter")
    @pytest.mark.parametrize("status",
                             ["active", "bankrupt", "closed", "test"])
    def test_issues_get_company_list_by_invalid_status(self, issues, status):
        params = {"status": status}
        response = issues.get_issues_companies(params)
        Asserts(response) \
            .status_code_should_be(HTTPStatus.UNPROCESSABLE_ENTITY) \
            .have_value_in_key("detail[0].msg", "value is not a valid enumeration member; permitted: 'ACTIVE', 'BANKRUPT', 'CLOSED'")