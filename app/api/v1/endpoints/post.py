"""
    POST ENDPOINTS
"""
from typing import Any, List

from fastapi import APIRouter, Depends, BackgroundTasks, Request, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models
from app.api import dependencies
from app.exception.base_exception import (
    post_not_found,
    post_not_found_by_user,
    user_not_found,
    category_not_found,
    tag_not_found,
)
from app.logger import logger

from app.schemas import PostCreate, PostDisplay, PostUpdate, PostDisplayDetailed

router = APIRouter()


@router.get("/{id}", response_model=PostDisplayDetailed)
async def get_post(
    request: Request,
    id: int,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for getting a post
    """

    post = crud.post.get(db_session, id_value=id)

    if not post:
        logger.error("Post with id %s not found", id)
        raise post_not_found

    return post


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
    current_user: models.User = Depends(dependencies.get_current_user),
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
    current_user: models.User = Depends(dependencies.get_current_user),
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
    current_user: models.User = Depends(dependencies.get_current_user),
):
    """
    API for deleting a post
    """

    post = crud.post.get(db_session, id_value=id)

    if not post:
        logger.error("Post with id %s not found", id)
        raise post_not_found

    post = crud.post.remove(db_session, id=id)

    return post


@router.get("/search", response_model=List[PostDisplayDetailed])
async def search_post(
    request: Request,
    keyword: str,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for searching a post
    """

    posts = crud.post.search(db_session, keyword=keyword)

    return posts


@router.get("/byUser/{user_id}", response_model=List[PostDisplay])
async def get_posts_by_user(
    request: Request,
    user_id: int,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for getting all posts by user
    """

    user = crud.user.get(db_session, id_value=user_id)

    if not user:
        logger.error("User with id %s not found", user_id)
        raise user_not_found

    posts = crud.post.get_multi_by_user(db_session, user_id=user_id)

    if not posts:
        logger.error("Post with user id %s not found", user_id)
        raise post_not_found_by_user

    return posts


@router.get("/byCategory/{category_id}", response_model=List[PostDisplay])
async def get_posts_by_category(
    request: Request,
    category_id: int,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for getting all posts by category
    """

    category = crud.category.get(db_session, id_value=category_id)

    if not category:
        logger.error("Category with id %s not found", category_id)
        raise category_not_found

    posts = crud.post.get_multi_by_category(db_session, category_id=category_id)

    return posts


@router.get("/byTag/{tag_id}", response_model=List[PostDisplay])
async def get_posts_by_tag(
    request: Request,
    tag_id: int,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for getting all posts by tag
    """

    tag = crud.tag.get(db_session, id_value=tag_id)

    if not tag:
        logger.error("Tag with id %s not found", tag_id)
        raise tag_not_found

    posts = crud.post.get_multi_by_tag(db_session, tag_id=tag_id)

    return posts
