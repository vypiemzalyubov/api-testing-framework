import allure
from api.api_client import ApiClient


class CompaniesApi(ApiClient):

    _URL = "https://send-request.me"
    _ENDPOINT = "/api/companies/"

    @allure.step('Обращение к /companies/')
    def companies(self, params: dict = None):
        return self.get(url=self._URL,
                        endpoint=self._ENDPOINT, params=params)
