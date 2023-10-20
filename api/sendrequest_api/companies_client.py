import allure
from httpx import Response
from api.api_client import ApiClient
from api.routes import ApiRoutes


class CompaniesClient(ApiClient):

    @allure.step("Getting companies")
    def get_companies(self, params: dict = None) -> Response:
        return self.get(url=f"{ApiRoutes.COMPANIES}/",
                        params=params)

    @allure.step("Getting company by id {company_id}")
    def get_company(self, company_id: int, headers: dict = None) -> Response:
        return self.get(url=f"{ApiRoutes.COMPANIES}/{company_id}",
                        headers=headers)
