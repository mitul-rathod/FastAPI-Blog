"""
    CRUD CATEGORY FILE
"""
import logging
from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base_crud import CRUDBase
from app.models import Category
from app.schemas import CategoryCreate, CategoryUpdate, CategoryDisplay

# get root logger
logger = logging.getLogger(__name__)


class CRUDCategory(CRUDBase[Category, CategoryCreate, CategoryUpdate]):
    """
    CRUD CLASS - CATEGORY
    """

    def create(self, db_session: Session, *, obj_in: CategoryCreate) -> Category:
        """
        Method to Create a new category object
        """
        db_obj = Category(
            name=obj_in.name,
            description=obj_in.description,
        )
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj


category = CRUDCategory(Category)
