"""
    CRUD TAG FILE
"""
import logging
from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base_crud import CRUDBase
from app.models import Post, Tag
from app.schemas import PostCreate, PostUpdate, PostDisplay

# get root logger
logger = logging.getLogger(__name__)


class CRUDCategory(CRUDBase[Post, PostCreate, PostUpdate]):
    """
    CRUD CLASS - POST
    """

    def create(self, db_session: Session, *, obj_in: PostCreate) -> Post:
        """
        Method to create a new object
        """
        db_obj = Post(
            title=obj_in.title,
            body=obj_in.body,
            category_id=obj_in.category_id,
            author_id=obj_in.author_id,
            tags=db_session.query(Tag).filter(Tag.id.in_(obj_in.tags)).all(),
        )
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj


post = CRUDCategory(Post)
