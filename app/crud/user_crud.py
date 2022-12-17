"""
    CRUD USER FILE
"""
import logging
from typing import Any, Dict, Optional, Union, List
from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base_crud import CRUDBase
from app.models.user_models import User
from app.schemas.user_schema import UserCreate, UserUpdate, UserDisplay

# get root logger
logger = logging.getLogger(__name__)


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    """
    CRUD CLASS - USER
    """

    def get_by_email(self, db_session: Session, *, email: str) -> Optional[User]:
        """
        Method to retrieve user by email
        """
        return db_session.query(User).filter(User.email == email).first()

    def get_by_id(self, db_session: Session, *, id_value: int) -> Optional[User]:
        """
        Method to retrieve user by id
        """
        return db_session.query(User).filter(User.id == id_value).first()

    def create(self, db_session: Session, *, obj_in: UserCreate) -> User:
        """
        Method to Create a new user object
        """
        db_obj = User(
            first_name=obj_in.first_name,
            last_name=obj_in.last_name,
            email=obj_in.email,
            password=get_password_hash(obj_in.password),
            is_admin=obj_in.is_admin,
            username=obj_in.username,
            gender=obj_in.gender,
        )
        db_session.add(db_obj)
        db_session.commit()
        db_session.refresh(db_obj)
        return db_obj

    def update(
        self,
        db_session: Session,
        *,
        db_obj: User,
        obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        """
        Method to Update a user object
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db_session, db_obj=db_obj, obj_in=update_data)

    def authenticate(
        self, db_session: Session, *, email: str, password: str
    ) -> Optional[User]:
        """
        Method to Authenticate user
        """
        user_exist = self.get_by_email(db_session, email=email)
        if not user_exist:
            return None
        if not verify_password(password, user_exist.password):
            return None
        return user_exist

    def is_admin(self, user_value: User) -> bool:
        """
        Method to Check if user is admin
        """
        return user_value.is_admin


user = CRUDUser(User)
