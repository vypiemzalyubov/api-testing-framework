import allure
from httpx import Response
from api.api_client import ApiClient
from api.routes import ApiRoutes


class IssuesClient(ApiClient):

    @allure.step("Getting companies with issue")
    def get_issues_companies(self, params: dict = None) -> Response:
        return self.get(endpoint=f"{ApiRoutes.ISSUES_COMPANIES}/",
                        params=params)

    @allure.step("Getting company by id {company_id} with sleep")
    def get_issues_company(self, company_id: int, headers: dict = None) -> Response:
        return self.get(endpoint=f"{ApiRoutes.ISSUES_COMPANIES}/{company_id}",
                        headers=headers)

    @allure.step("Getting one user by id {user_id} without params")
    def get_issues_user(self, user_id: int = None, headers: dict = None) -> Response:
        return self.get(endpoint=f"{ApiRoutes.ISSUES_USERS}/{user_id}",
                        headers=headers)

    @allure.step("Creating user with ignored params")
    def create_issues_user(self, payload: dict, headers: dict = None) -> Response:
        return self.post(endpoint=f"{ApiRoutes.ISSUES_USERS}/",
                         json=payload,
                         headers=headers)
