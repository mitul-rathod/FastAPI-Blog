"""
    POST ENDPOINTS
"""
from typing import Any, List

from fastapi import APIRouter, Depends, BackgroundTasks, Request, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, schemas
from app.api import dependencies
from app.exception.base_exception import post_not_found
from app.logger import logger

from app.schemas import PostCreate, PostDisplay, PostUpdate


router = APIRouter()


@router.get("/", response_model=List[PostDisplay])
async def get_posts(
    request: Request,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for getting all posts
    """
    posts = crud.post.get_multi_without_limit(db_session)

    return posts


@router.post("/create", response_model=PostDisplay)
async def create_post(
    request: Request,
    post_in: PostCreate,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for creating a new post
    """

    post = crud.post.create(db_session, obj_in=post_in)

    return post


@router.patch("/update", response_model=PostDisplay)
async def update_post(
    request: Request,
    post_in: PostUpdate,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for updating a post
    """

    db_obj = crud.post.get(db_session, id_value=post_in.id)

    if not db_obj:
        logger.error("Post with id %s not found", post_in.id)
        return post_not_found

    post = crud.post.update(db_session, db_obj=db_obj, obj_in=post_in)

    return post


@router.delete("/delete/{id}", response_model=PostDisplay)
async def delete_post(
    request: Request,
    id: int,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for deleting a post
    """

    post = crud.post.remove(db_session, id_value=id)

    return post
