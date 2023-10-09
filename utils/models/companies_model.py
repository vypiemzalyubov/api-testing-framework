from typing import List, Optional
from enum import Enum
from pydantic import BaseModel


class CompanyStatus(str, Enum):
    ACTIVE = "ACTIVE"
    BANKRUPT = "BANKRUPT"
    CLOSED = "CLOSED"


class CompanyData(BaseModel):
    company_id: int
    company_name: str
    company_address: str
    company_status: CompanyStatus


class MetaData(BaseModel):
    limit: int
    offset: int
    total: int


class CompanyList(BaseModel):
    data: List[CompanyData]
    meta: MetaData


class DescriptionLang(BaseModel):
    translation_lang: str
    translation: str


class Company(CompanyData):
    description_lang: Optional[List[DescriptionLang]] = None
    description: Optional[str] = None
