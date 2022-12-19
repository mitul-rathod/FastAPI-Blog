"""
    USER ENDPOINTS
"""
from typing import Any, List

from fastapi import APIRouter, Depends, BackgroundTasks, Request, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import dependencies
from app.logger import logger
from app.exception.base_exception import user_found, invalid_password, user_not_found
from app.schemas.user_schema import UserDisplay
from app.utils import (
    is_email_valid,
    is_valid_password,
)


router = APIRouter()


@router.get("/", response_model=List[UserDisplay])
async def get_users(
    request: Request,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for getting all users
    """
    users = jsonable_encoder(crud.user.get_multi(db_session))

    return users


@router.post("/create", response_model=UserDisplay)
async def create_user(
    request: Request,
    user_in: schemas.UserCreate,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for creating a new user
    """

    user_in.email = is_email_valid(email=user_in.email)

    user = crud.user.get_by_email(db_session, email=user_in.email)
    if user:
        logger.warning("User with email %s already exist", user_in.email)
        raise user_found

    if not is_valid_password(user_in.password):
        logger.error("Password %s is not valid", user_in.password)
        raise invalid_password

    user = jsonable_encoder(crud.user.create(db_session, obj_in=user_in))

    return user


@router.patch("/update", response_model=UserDisplay)
async def update_user(
    request: Request,
    user_in: schemas.UserUpdate,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for updating a user
    """
    user = crud.user.get_by_id(db_session, id_value=user_in.id)
    if not user:
        logger.error("User with id %s not found", user_in.id)
        raise user_not_found

    user = jsonable_encoder(crud.user.update(db_session, db_obj=user, obj_in=user_in))

    return user


@router.delete("/delete/{id}", response_model=UserDisplay)
async def delete_user(
    request: Request,
    id: int,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for deleting a user
    """
    user = crud.user.get_by_id(db_session, id_value=id)
    if not user:
        logger.error("User with id %s not found", id)
        raise user_not_found

    user = jsonable_encoder(crud.user.remove(db_session, id_value=id))

    return user
