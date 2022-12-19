"""
    TAG ENDPOINTS
"""
from typing import Any, List

from fastapi import APIRouter, Depends, BackgroundTasks, Request, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models
from app.api import dependencies
from app.exception.base_exception import tag_not_found
from app.logger import logger

from app.schemas import TagCreate, TagDisplay, TagUpdate


router = APIRouter()


@router.get("/", response_model=List[TagDisplay])
async def get_tags(
    request: Request,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for getting all categories
    """
    tags = jsonable_encoder(crud.tag.get_multi_without_limit(db_session))

    return tags


@router.post("/create", response_model=TagDisplay)
async def create_tag(
    request: Request,
    tag_in: TagCreate,
    db_session: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    """
    API for creating a new tag
    """

    tag = jsonable_encoder(crud.tag.create(db_session, obj_in=tag_in))

    return tag


@router.patch("/update", response_model=TagDisplay)
async def update_tag(
    request: Request,
    tag_in: TagUpdate,
    db_session: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    """
    API for updating a tag
    """

    db_obj = crud.tag.get(db_session, id_value=tag_in.id)

    if not db_obj:
        logger.error("Tag with id %s not found", tag_in.id)
        return tag_not_found

    tag = jsonable_encoder(crud.tag.update(db_session, db_obj=db_obj, obj_in=tag_in))

    return tag


@router.delete("/delete/{id}", response_model=TagDisplay)
async def delete_tag(
    request: Request,
    id: int,
    db_session: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    """
    API for deleting a tag
    """

    tag = crud.tag.get(db_session, id_value=id)

    if not tag:
        logger.error("Tag with id %s not found", id)
        raise tag_not_found

    tag = jsonable_encoder(crud.tag.remove(db_session, id_value=id))

    return tag


@router.get("/search", response_model=List[TagDisplay])
async def search_tag(
    request: Request,
    keyword: str,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for searching a tag
    """

    tags = jsonable_encoder(crud.tag.search(db_session, keyword=keyword))

    return tags
