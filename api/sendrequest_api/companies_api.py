import allure
from api.api_client import ApiClient
from api.routes import ApiRoutes


class CompaniesApi(ApiClient):

    @allure.step("Getting all companies")
    def get_companies(self, params: dict = None, headers: dict = None):
        return self.get(endpoint=f"{ApiRoutes.COMPANIES}/", params=params, headers=headers)

    @allure.step("Getting company with id {company_id}")
    def get_company(self, company_id: int, headers: dict = None):
        return self.get(endpoint=f"{ApiRoutes.COMPANIES}/{company_id}", headers=headers)
