from pydantic import BaseModel


class Token(BaseModel):
    token: str


class AuthUser(BaseModel):
    user_name: str
    email_address: str
    valid_till: str
