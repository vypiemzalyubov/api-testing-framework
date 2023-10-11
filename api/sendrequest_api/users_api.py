import allure
from api.api_client import ApiClient


class UsersApi(ApiClient):

    _ENDPOINT = "/api/users/"

    @allure.step("Request to API /users/")
    def users(self, user_id: int = "", params: dict = None, headers: dict = None):
        return self.get(endpoint=f"{self._ENDPOINT}{user_id}", params=params, headers=headers)
