from enum import Enum


class ApiRoutes(str, Enum):
    COMPANIES = "/companies"
    USERS = "/users"
    AUTH_AUTORIZE = "/auth/authorize"
    AUTH_ME = "/auth/me"
    ISSUES_COMPANIES = "/issues/companies"
    ISSUES_USERS = "/issues/users"

    def __str__(self) -> str:
        return self.value
