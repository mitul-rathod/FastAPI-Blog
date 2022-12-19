"""
    CRUD TAG FILE
"""
import logging
from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base_crud import CRUDBase
from app.models import Tag
from app.schemas import TagCreate, TagUpdate, TagDisplay

# get root logger
logger = logging.getLogger(__name__)


class CRUDCategory(CRUDBase[Tag, TagCreate, TagUpdate]):
    """
    CRUD CLASS - TAG
    """

    def create(self, db_session: Session, *, obj_in: TagCreate) -> Tag:
        """
        Method to Create a new tag object
        """
        db_obj = Tag(
            name=obj_in.name,
            description=obj_in.description,
        )
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj


tag = CRUDCategory(Tag)
