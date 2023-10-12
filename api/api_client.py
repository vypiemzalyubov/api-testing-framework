import os
import allure
import httpx
from httpx import Client, Response
from dotenv import load_dotenv
from utils.logger import log

load_dotenv()


class ApiClient(Client):

    _BASE_URL = os.getenv("BASE_URL")
    _TIMEOUT = 10

    def __init__(self) -> None:
        self.response = None

    # @allure.step("Sending a GET request to \"{self._BASE_URL}\"")
    def get(self, endpoint: str, params: dict = None, headers: dict = None) -> Response:
        with httpx.Client() as client:
            self.response = client.get(url=f"{self._BASE_URL}{endpoint}",
                                       params=params,
                                       headers=headers,
                                       timeout=self._TIMEOUT)
        log(response=self.response)
        return self.response

    # @allure.step("Sending a POST request to \"{self._BASE_URL}\"")
    def post(self, endpoint: str, data: dict = None, headers: dict = None) -> Response:
        with httpx.Client() as client:
            self.response = client.post(url=f"{self._BASE_URL}{endpoint}",
                                        json=data,
                                        headers=headers,
                                        timeout=self._TIMEOUT)
        log(response=self.response, request_body=data)
        return self.response

    # @allure.step("Sending a PUT request to \"{self._BASE_URL}\"")
    def put(self, endpoint: str, data: dict = None, headers: dict = None) -> Response:
        with httpx.Client() as client:
            self.response = client.put(url=f"{self._BASE_URL}{endpoint}",
                                       json=data,
                                       headers=headers,
                                       timeout=self._TIMEOUT)
        log(response=self.response, request_body=data)
        return self.response

    # @allure.step("Sending a DELETE request to \"{self._BASE_URL}\"")
    def delete(self, endpoint: str, params: str = None, headers: dict = None) -> Response:
        with httpx.Client() as client:
            self.response = client.get(url=f"{self._BASE_URL}{endpoint}",
                                       params=params,
                                       headers=headers,
                                       timeout=self._TIMEOUT)
        log(response=self.response)
        return self.response
