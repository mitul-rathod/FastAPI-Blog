"""
    USER MODEL FILE
"""
from sqlalchemy.sql import func
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime
from sqlalchemy.ext.declarative import declared_attr

from app.db.base_class import Base


class User(Base):
    """
    User Model
    """

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    is_admin = Column(Boolean(), default=False)
    gender = Column(String)
    created = Column(DateTime(timezone=True), server_default=func.now())
    updated = Column(DateTime(timezone=True), onupdate=func.now())


    @declared_attr
    def __searchable__(self) -> list:
        return ["first_name", "last_name", "email", "username"]
