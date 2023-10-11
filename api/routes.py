from enum import Enum


class ApiRoutes(str, Enum):
    COMPANIES = "/api/companies"
    USERS = "/api/users"
    AUTH_AUTORIZE = "/api/auth/authorize"
    AUTH_ME = "/api/auth/me"
    ISSUES_COMPANY = "/api/issues/companies"
    ISSUES_USERS = "/api/issues/users"

    def __str__(self) -> str:
        return self.value
