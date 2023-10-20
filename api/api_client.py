from typing import Any
import allure
from httpx import Client, Response
from httpx._client import UseClientDefault
from httpx._types import (AuthTypes, CookieTypes, HeaderTypes, QueryParamTypes,
                          RequestContent, RequestData, RequestExtensions,
                          RequestFiles, TimeoutTypes, URLTypes)
from settings import base_settings
from utils.logger import log


class ApiClient(Client):

    def __init__(self) -> None:
        super().__init__(base_url=base_settings.api_url)

    @allure.step(f"Sending a GET request to \"{Client.base_url}\"")
    def get(
        self,
        url: URLTypes,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = None,
        follow_redirects: bool | UseClientDefault = None,
        timeout: TimeoutTypes | UseClientDefault = None,
        extensions: RequestExtensions | None = None
    ) -> Response:
        self.response = super().get(
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions
        )
        log(response=self.response)
        return self.response

    @allure.step(f"Sending a POST request to \"{Client.base_url}\"")
    def post(
        self,
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = None,
        follow_redirects: bool | UseClientDefault = None,
        timeout: TimeoutTypes | UseClientDefault = None,
        extensions: RequestExtensions | None = None
    ) -> Response:
        self.response = super().post(
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions
        )
        log(response=self.response, request_body=json)
        return self.response

    @allure.step(f"Sending a PUT request to \"{Client.base_url}\"")
    def put(
        self,
        url: URLTypes,
        *,
        content: RequestContent | None = None,
        data: RequestData | None = None,
        files: RequestFiles | None = None,
        json: Any | None = None,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = None,
        follow_redirects: bool | UseClientDefault = None,
        timeout: TimeoutTypes | UseClientDefault = None,
        extensions: RequestExtensions | None = None
    ) -> Response:
        self.response = super().put(
            url=url,
            content=content,
            data=data,
            files=files,
            json=json,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions
        )
        log(response=self.response, request_body=json)
        return self.response

    @allure.step(f"Sending a DELETE request to \"{Client.base_url}\"")
    def delete(
        self,
        url: URLTypes,
        *,
        params: QueryParamTypes | None = None,
        headers: HeaderTypes | None = None,
        cookies: CookieTypes | None = None,
        auth: AuthTypes | UseClientDefault = None,
        follow_redirects: bool | UseClientDefault = None,
        timeout: TimeoutTypes | UseClientDefault = None,
        extensions: RequestExtensions | None = None
    ) -> Response:
        self.response = super().delete(
            url=url,
            params=params,
            headers=headers,
            cookies=cookies,
            auth=auth,
            follow_redirects=follow_redirects,
            timeout=timeout,
            extensions=extensions
        )
        log(response=self.response)
        return self.response
