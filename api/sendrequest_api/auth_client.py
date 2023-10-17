import allure
from httpx import Response
from api.api_client import ApiClient
from api.routes import ApiRoutes


class AuthClient(ApiClient):

    @allure.step("Getting auth token")
    def create_auth_token(self, data: dict = None, headers: dict = None) -> Response:
        return self.post(url=f"{ApiRoutes.AUTH_AUTORIZE}",
                         json=data,
                         headers=headers)

    @allure.step("Getting user data by token")
    def auth_user(self, headers: dict = None) -> Response:
        return self.get(url=f"{ApiRoutes.AUTH_ME}",
                        headers=headers)