from typing import List
from pydantic import BaseModel


class MetaData(BaseModel):
    limit: int
    offset: int
    total: int


class UserData(BaseModel):
    first_name: str | None = None
    last_name: str
    company_id: int | None = None
    user_id: int


class UserList(BaseModel):
    data: List[UserData]
    meta: MetaData
