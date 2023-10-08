import allure
from api.api_client import ApiClient


class CompaniesApi(ApiClient):

    _ENDPOINT = "/api/companies/"

    @allure.step('Request to API /companies/')
    def companies(self, params: dict = None, headers: dict = None):
        return self.get(endpoint=self._ENDPOINT, params=params, headers=headers)
