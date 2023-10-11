import allure
from api.api_client import ApiClient


class CompaniesApi(ApiClient):

    _ENDPOINT = "/api/companies/"

    @allure.step("Request to API /companies/")
    def companies(self, company_id: int = "", params: dict = None, headers: dict = None):
        return self.get(endpoint=f"{self._ENDPOINT}{company_id}", params=params, headers=headers)