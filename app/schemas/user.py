from pydantic import BaseModel

from typing import Optional


class UserBase(BaseModel):
    id: int

class UserCreate(BaseModel):
    password: str
    username: str
    # email: str

class UserUpdate(BaseModel):
    fullname: str
    nickname: str

class UserShow(UserBase):
    fullname: Optional[str] = None
    username:str

class UserDelete(UserBase):
    pass