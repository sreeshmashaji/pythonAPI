from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr
from pydantic.types import conint


class Usercreate(BaseModel):
    email:EmailStr
    password:str
    phoneNumber:int


class UserResponse(BaseModel):
    id:int
    email:str
    phoneNumber:int
    created_at:datetime
    class Config:
        orm_mode=True


class BasePost(BaseModel):
    title:str
    content:str
    published:bool=True

class Create_post(BasePost):
    pass

class Post(BaseModel):
    id:int
    title:str
    content:str
    published:bool=True
    created_at:datetime
    user_id:int
    owner:UserResponse
    class Config:
        orm_mode=True

class Postvote(BaseModel):
    Post:Post
    votes:int
    class Config:
        orm_mode=True





class UserLogin(BaseModel):
    email:EmailStr
    password:str
    mobileNumber:int
    class Config:
        orm_mode=True

class Token(BaseModel):
    access_toke:str
    access_type:str
    

class TokenData(BaseModel):
    id:Optional[str]=None


class Vote(BaseModel):
    post_id:int
    dir:conint(le=1)