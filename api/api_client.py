import allure
import requests
from requests import Response
from utils.logger import log


class ApiClient:

    _HEADERS = None
    _COOKIES = None
    _TIMEOUT = 10

    def __init__(self):
        self.response = None

    @allure.step("Sending a GET request")
    def get(self, url: str, endpoint: str, params: dict = None) -> Response:
        if params is not None:
            params = {**params}
        else:
            params = {}
        with allure.step(f"GET request for url: {url}{endpoint}\n"
                         f"Request parameters: {params}"):
            self.response = requests.get(url=f"{url}{endpoint}",
                                         params=params,
                                         headers=self._HEADERS,
                                         cookies=self._COOKIES,
                                         timeout=self._TIMEOUT)
        log(response=self.response)
        return self.response

    @allure.step("Sending a POST request")
    def post(self, url: str, endpoint: str, data: dict = None) -> Response:
        with allure.step(f"POST request for url: {url}{endpoint}\n"
                         f"Request body: \n {data}"):
            self.response = requests.post(url=f"{url}{endpoint}",
                                          json=data,
                                          headers=self._HEADERS,
                                          cookies=self._COOKIES,
                                          timeout=self._TIMEOUT)
        log(response=self.response, request_body=data)
        return self.response

    @allure.step("Sending a PUT request")
    def put(self, url: str, endpoint: str, data: dict = None) -> Response:
        with allure.step(f"PUT request for url: {url}{endpoint}\n"
                         f"Request body: \n {data}"):
            self.response = requests.put(url=f"{url}{endpoint}",
                                         json=data,
                                         headers=self._HEADERS,
                                         cookies=self._COOKIES,
                                         timeout=self._TIMEOUT)
        log(response=self.response, request_body=data)
        return self.response

    @allure.step("Sending a DELETE request")
    def delete(self, url: str, endpoint: str, params: str = None) -> Response:
        with allure.step(f"DELETE request for url: {url}{endpoint}\n"
                         f"Request parameters: {params}"):
            self.response = requests.get(url=f"{url}{endpoint}",
                                         params=params,
                                         headers=self._HEADERS,
                                         cookies=self._COOKIES,
                                         timeout=self._TIMEOUT)
        log(response=self.response)
        return self.response
