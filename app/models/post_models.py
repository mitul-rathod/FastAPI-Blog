"""
    POST MODEL FILE
"""
from sqlalchemy.sql import func
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Table, ARRAY
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.mutable import MutableList

from app.db.base_class import Base


post_tag = Table(
    "post_tag",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id")),
    Column("tag_id", Integer, ForeignKey("tag.id")),
)


class Category(Base):
    """
    Category Model
    """

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    posts = relationship("Post", back_populates="category")

    @declared_attr
    def __searchable__(self) -> list:
        return ["name", "description"]


class Tag(Base):
    """
    Tag Model
    """

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    description = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    posts = relationship("Post", secondary=post_tag, back_populates="tags")

    @declared_attr
    def __searchable__(self) -> list:
        return ["name", "description"]


class Post(Base):
    """
    Post Model
    """

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(50), unique=True, index=True)
    body = Column(String(255))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    # Relationships
    author_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    author = relationship("User", back_populates="posts")

    category_id = Column(Integer, ForeignKey("category.id", ondelete="CASCADE"))
    category = relationship("Category", back_populates="posts")

    tags = relationship("Tag", secondary=post_tag, back_populates="posts")

    @declared_attr
    def __searchable__(self) -> list:
        return ["title", "body"]
