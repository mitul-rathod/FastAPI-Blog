"""
    LOGIN ENDPOINTS
"""
from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import dependencies
from app.core import security
from app.core.configuration import settings
from app.core.security import get_password_hash
from app.exception.base_exception import invalid_credentials

router = APIRouter()


@router.post("/", response_model=schemas.Token)
def login_access_token(
    db: Session = Depends(dependencies.get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Any:
    """
    API for generating access token
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise invalid_credentials
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/test-token", response_model=schemas.UserDisplay)
def test_token(
    current_user: models.User = Depends(dependencies.get_current_user),
) -> Any:
    """
    Test access token
    """
    return jsonable_encoder(current_user)
