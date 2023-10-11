from typing import List
from enum import Enum
from pydantic import BaseModel


class CompanyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    BANKRUPT = "BANKRUPT"
    CLOSED = "CLOSED"


class MetaData(BaseModel):
    limit: int
    offset: int
    total: int


class CompanyData(BaseModel):
    company_id: int
    company_name: str
    company_address: str
    company_status: CompanyStatus


class DescriptionLang(BaseModel):
    translation_lang: str
    translation: str


class CompanyList(BaseModel):
    data: List[CompanyData]
    meta: MetaData


class Company(CompanyData):
    description_lang: List[DescriptionLang] | None = None
    description: str | None = None
