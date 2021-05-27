from typing import Optional
from pydantic import BaseModel


class User(BaseModel):
    id_user: Optional[int]
    name: str
    last_name: str
    email: str
    password: str

    class Config:
        orm_mode = True
        

class UserLogin(BaseModel):
    email: str
    password : str

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: str

    class Config:
        orm_mode = True

class Dog(BaseModel):
    id_dog: Optional[int]
    name: str
    picture: str
    is_adopted: bool
    create_date: str
    id_user : int

    class Config:
        orm_mode = True
        #arbitrary_types_allowed = True

class CreateByName(BaseModel):
    #name : str
    is_adopted: int
    id_user : int
    
    class Config:
        orm_mode=True


class UpdateByName(BaseModel):
    name : str
    is_adopted: int
    id_user: int

    class Config:
        orm_mode = True


class Response( BaseModel):
    message: str
    
