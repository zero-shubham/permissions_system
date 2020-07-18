from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    user_id: str
    group: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str


class LogoutResponse(BaseModel):
    logged_out: bool


class ValidateResponse(BaseModel):
    valid: bool


class LoginForm(BaseModel):
    username: str
    password: str
    grant_type: str
    client_id: Optional[str]
    client_secret: Optional[str]


class Logout(BaseModel):
    user_id: UUID
