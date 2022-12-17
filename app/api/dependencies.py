"""
    DEPENDENCIES FILE FOR ROUTES
"""
from typing import Generator
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.core import security
from app.core.configuration import settings
from app.db.session import SessionLocal
from app.exception.base_exception import invalid_credentials, user_not_found

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")


def get_db() -> Generator:
    """
    Returns a new database session
    """
    try:
        db_session = SessionLocal()
        yield db_session
    finally:
        db_session.close()


def get_current_user(
    db_session: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    """
    Return the current user
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )

        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError) as excep:
        raise invalid_credentials from excep

    user = crud.user.get(db_session, id_value=token_data.sub)
    if not user:
        raise user_not_found
    return user
