from pydantic import BaseModel, validator
from typing import Optional
from uuid import UUID


class UserBase(BaseModel):
    user_name: str
    group: str


class UserInDB(UserBase):
    password: str


class UserInResp(UserBase):
    id: UUID


class UserInDbUpdate(BaseModel):
    user_name: Optional[str]
    group: Optional[str]
    password: Optional[str]

    @validator('*', pre=True)
    def split_str(cls, v):
        if v:
            return v


class UserDeleteResp(BaseModel):
    deleted: bool
