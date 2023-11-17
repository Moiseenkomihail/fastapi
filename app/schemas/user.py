from pydantic import BaseModel

from typing import Optional


class UserBase(BaseModel):
    pass

class UserCreate(BaseModel):
    password: str
    username: str
    # email: str

class UserUpdate(BaseModel):
    fullname: str
    nickname: str

class UserShow(BaseModel):
    fullname: Optional[str] = None
    id: int
    username:str

class UserDelete(BaseModel):
    id: int