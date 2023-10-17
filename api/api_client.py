import allure
from httpx import Client, Response
from settings import base_settings
from utils.logger import log


class ApiClient(Client):

    def __init__(self) -> None:
        super().__init__(base_url=base_settings.api_url)

    @allure.step(f"Sending a GET request to \"{Client.base_url}\"")
    def get(
        self,
        url: str,
        params: dict = None,
        headers: dict = None,
        cookies: dict = None,
        follow_redirects: bool = None,
        timeout: int = None
    ) -> Response:
        self.response = super().get(
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            follow_redirects=follow_redirects,
            timeout=timeout
        )
        log(response=self.response)
        return self.response

    @allure.step(f"Sending a POST request to \"{Client.base_url}\"")
    def post(
        self,
        url: str,
        json: dict = None,
        headers: dict = None,
        cookies: dict = None,
        follow_redirects: bool = None,
        timeout: int = None
    ) -> Response:
        self.response = super().post(
            url=url,
            json=json,
            headers=headers,
            cookies=cookies,
            follow_redirects=follow_redirects,
            timeout=timeout
        )
        log(response=self.response, request_body=json)
        return self.response

    @allure.step(f"Sending a PUT request to \"{Client.base_url}\"")
    def put(
        self,
        url: str,
        json: dict = None,
        headers: dict = None,
        cookies: dict = None,
        follow_redirects: bool = None,
        timeout: int = None
    ) -> Response:
        self.response = super().put(
            url=url,
            json=json,
            headers=headers,
            cookies=cookies,
            follow_redirects=follow_redirects,
            timeout=timeout
        )
        log(response=self.response, request_body=json)
        return self.response

    @allure.step(f"Sending a DELETE request to \"{Client.base_url}\"")
    def delete(
        self,
        url: str,
        params: str = None,
        headers: dict = None,
        cookies: dict = None,
        follow_redirects: bool = None,
        timeout: int = None
    ) -> Response:
        self.response = super().delete(
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            follow_redirects=follow_redirects,
            timeout=timeout
        )
        log(response=self.response)
        return self.response
