import allure
from httpx import Response
from api.api_client import ApiClient
from api.routes import ApiRoutes


class UsersClient(ApiClient):

    @allure.step("Getting users list")
    def get_users(self, params: dict = None, headers: dict = None) -> Response:
        return self.get(url=f"{ApiRoutes.USERS}/",
                        params=params,
                        headers=headers)

    @allure.step("Creating user")
    def create_user(self, payload: dict, headers: dict = None) -> Response:
        return self.post(url=f"{ApiRoutes.USERS}/",
                         json=payload,
                         headers=headers)

    @allure.step("Getting one user by id {user_id}")
    def get_user(self, user_id: int = None, headers: dict = None) -> Response:
        return self.get(url=f"{ApiRoutes.USERS}/{user_id}",
                        headers=headers)

    @allure.step("Updating user by id {user_id}")
    def update_user(self, user_id: int, payload: dict, headers: dict = None) -> Response:
        return self.put(url=f"{ApiRoutes.USERS}/{user_id}",
                        json=payload,
                        headers=headers)

    @allure.step("Deleting user by id {user_id}")
    def delete_user(self, user_id: int = None, headers: dict = None) -> Response:
        return self.delete(url=f"{ApiRoutes.USERS}/{user_id}",
                           headers=headers)
