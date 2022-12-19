"""
    POST SCHEMA FILE
"""
from typing import Optional, List
from pydantic import BaseModel, EmailStr

from app.models.enum_class_models import GenderEnum
from app.schemas import UserDisplay


class CategoryBase(BaseModel):
    """
    Category Base Schema
    """

    name: str

    class Config:
        orm_mode = True


class CategoryCreate(CategoryBase):
    """
    Category Create Schema
    """

    description: Optional[str] = None


class CategoryUpdate(CategoryBase):
    """
    Category Update Schema
    """

    id: int
    description: Optional[str] = None


class CategoryDisplay(CategoryBase):
    """
    Category Display Schema
    """

    id: int


class TagBase(BaseModel):
    """
    Tag Base Schema
    """

    name: str

    class Config:
        orm_mode = True


class TagCreate(TagBase):
    """
    Tag Create Schema
    """

    description: Optional[str] = None

    class Config:
        orm_mode = True


class TagUpdate(TagBase):
    """
    Tag Update Schema
    """

    id: int
    description: Optional[str] = None

    class Config:
        orm_mode = True


class TagDisplay(TagBase):
    """
    Tag Display Schema
    """

    id: int

    class Config:
        orm_mode = True


class PostBase(BaseModel):
    """
    Post Base Schema
    """

    title: str
    category_id: int
    tags: List[int]
    author_id: int

    class Config:
        orm_mode = True


class PostCreate(PostBase):
    """
    Post Create Schema
    """

    body: str

    class Config:
        orm_mode = True


class PostUpdate(PostBase):
    """
    Post Update Schema
    """

    id: int
    body: str

    class Config:
        orm_mode = True


class PostDisplay(PostBase):
    """
    Post Display Schema
    """

    id: int
    category_id: int
    tags: List[TagDisplay]
    author_id: int

    class Config:
        orm_mode = True


class PostDisplayDetailed(PostDisplay):
    """
    Post Detailed Display Schema
    """

    body: str

    class Config:
        orm_mode = True
