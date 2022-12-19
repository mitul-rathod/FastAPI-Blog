"""
    USER SCHEMA FILE
"""
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.models.enum_class_models import GenderEnum


class UserBase(BaseModel):
    """
    User Base Schema
    """

    first_name: str
    last_name: str
    email: str

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class UserCreate(UserBase):
    """
    User Create Schema
    """

    email: str
    password: str
    is_admin: Optional[bool] = False
    gender: Optional[GenderEnum]
    username: Optional[str]


# Properties to receive via API on update
class UserUpdate(UserBase):
    """
    User Update Schema
    """

    id: str
    first_name: Optional[str]
    last_name: Optional[str]
    email: Optional[str]
    username: Optional[str]
    password: Optional[str] = None
    is_admin: Optional[bool] = False
    gender: Optional[GenderEnum]


class UserDisplay(UserBase):
    """
    User Display Schema
    """

    id: str
    username: Optional[str]
