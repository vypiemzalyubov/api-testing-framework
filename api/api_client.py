import allure
from httpx import Client, Response
from settings import base_settings
from utils.logger import log


class ApiClient(Client):

    def __init__(self) -> None:
        super().__init__(base_url=base_settings.api_url)

    @allure.step(f"Sending a GET request to \"{Client.base_url}\"")
    def get(self, endpoint: str, params: dict = None, headers: dict = None, cookies: dict = None, timeout: int = None) -> Response:
        self.response = super().get(url=endpoint,
                                    params=params,
                                    headers=headers,
                                    cookies=cookies,
                                    timeout=timeout)
        log(response=self.response)
        return self.response

    @allure.step(f"Sending a POST request to \"{Client.base_url}\"")
    def post(self, endpoint: str, json: dict = None, headers: dict = None, cookies: dict = None, timeout: int = None) -> Response:
        self.response = super().post(url=endpoint,
                                     json=json,
                                     headers=headers,
                                     cookies=cookies,
                                     timeout=timeout)
        log(response=self.response, request_body=json)
        return self.response

    @allure.step(f"Sending a PUT request to \"{Client.base_url}\"")
    def put(self, endpoint: str, json: dict = None, headers: dict = None, cookies: dict = None, timeout: int = None) -> Response:
        self.response = super().put(url=endpoint,
                                    json=json,
                                    headers=headers,
                                    cookies=cookies,
                                    timeout=timeout)
        log(response=self.response, request_body=json)
        return self.response

    @allure.step(f"Sending a DELETE request to \"{Client.base_url}\"")
    def delete(self, endpoint: str, params: str = None, headers: dict = None, cookies: dict = None, timeout: int = None) -> Response:
        self.response = super().delete(url=endpoint,
                                       params=params,
                                       headers=headers,
                                       cookies=cookies,
                                       timeout=timeout)
        log(response=self.response)
        return self.response
