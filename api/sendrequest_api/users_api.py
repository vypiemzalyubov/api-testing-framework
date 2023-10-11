import os
import allure
from api.api_client import ApiClient
from api.routes import ApiRoutes


class UsersApi(ApiClient):

    @allure.step("Getting all users")
    def get_users(self, params: dict = None, headers: dict = None):
        return self.get(endpoint=f"{ApiRoutes.USERS}/", params=params, headers=headers)

    @allure.step("Getting company with id {user_id}")
    def get_user(self, user_id: int, headers: dict = None):
        return self.get(endpoint=f"{ApiRoutes.USERS}/{user_id}", headers=headers)