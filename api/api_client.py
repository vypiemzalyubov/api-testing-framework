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

    def __init__(self):
        self.response = None

    @allure.step("Sending a GET request")
    def get(self, endpoint: str, params: dict = None, headers: dict = None) -> Response:
        with allure.step(f"GET request for url: {self._BASE_URL}{endpoint}\n"
                         f"Request parameters: {params}"):
            with httpx.Client() as client:
                self.response = client.get(url=f"{self._BASE_URL}{endpoint}",
                                           params=params,
                                           headers=headers,
                                           timeout=self._TIMEOUT)
        log(response=self.response)
        return self.response

    @allure.step("Sending a POST request")
    def post(self, url: str, endpoint: str, data: dict = None, headers: dict = None) -> Response:
        with allure.step(f"POST request for url: {url}{endpoint}\n"
                         f"Request body: \n {data}"):
            with httpx.Client() as client:
                self.response = client.post(url=f"{url}{endpoint}",
                                            json=data,
                                            headers=headers,
                                            timeout=self._TIMEOUT)
        log(response=self.response, request_body=data)
        return self.response

    @allure.step("Sending a PUT request")
    def put(self, url: str, endpoint: str, data: dict = None, headers: dict = None) -> Response:
        with allure.step(f"PUT request for url: {url}{endpoint}\n"
                         f"Request body: \n {data}"):
            with httpx.Client() as client:
                self.response = client.put(url=f"{url}{endpoint}",
                                           json=data,
                                           headers=headers,
                                           timeout=self._TIMEOUT)
        log(response=self.response, request_body=data)
        return self.response

    @allure.step("Sending a DELETE request")
    def delete(self, url: str, endpoint: str, params: str = None, headers: dict = None) -> Response:
        with allure.step(f"DELETE request for url: {url}{endpoint}\n"
                         f"Request parameters: {params}"):
            with httpx.Client() as client:
                self.response = client.get(url=f"{url}{endpoint}",
                                           params=params,
                                           headers=headers,
                                           timeout=self._TIMEOUT)
        log(response=self.response)
        return self.response
