import allure
from httpx import Response
from api.api_client import ApiClient
from api.routes import ApiRoutes


class UsersClient(ApiClient):

    @allure.step("Getting all users")
    def get_users(self, params: dict = None, headers: dict = None) -> Response:
        return self.get(endpoint=f"{ApiRoutes.USERS}/",
                        params=params,
                        headers=headers)

    @allure.step("Creating user")
    def create_user(self, payload: dict, headers: dict = None) -> Response:
        return self.post(endpoint=f"{ApiRoutes.USERS}/",
                         json=payload,
                         headers=headers)

    @allure.step("Getting user with id {user_id}")
    def get_user(self, user_id: int = None, headers: dict = None) -> Response:
        return self.get(endpoint=f"{ApiRoutes.USERS}/{user_id}",
                        headers=headers)

    @allure.step("Updating user with id {user_id}")
    def update_user(self, user_id: int, payload: dict, headers: dict = None) -> Response:
        return self.put(endpoint=f"{ApiRoutes.USERS}/{user_id}",
                        json=payload,
                        headers=headers)

    @allure.step("Deleting user with id {user_id}")
    def delete_user(self, user_id: int = None, headers: dict = None) -> Response:
        return self.delete(endpoint=f"{ApiRoutes.USERS}/{user_id}",
                           headers=headers)
