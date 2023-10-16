from pydantic import BaseModel


class Token(BaseModel):
    token: str


class UserAuth(BaseModel):
    user_name: str
    email_address: str
    valid_till: str
