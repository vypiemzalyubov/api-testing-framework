from pydantic import BaseModel
from typing import List
from enum import Enum


class CompanyStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    BANKRUPT = 'BANKRUPT'
    CLOSED = 'CLOSED'


class CompanyData(BaseModel):
    company_id: int
    company_name: str
    company_address: str
    company_status: CompanyStatus


class MetaData(BaseModel):
    limit: int
    offset: int
    total: int


class Company(BaseModel):
    data: List[CompanyData]
    meta: MetaData
