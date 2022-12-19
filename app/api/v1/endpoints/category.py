"""
    CATEGORY ENDPOINTS
"""
from typing import Any, List

from fastapi import APIRouter, Depends, BackgroundTasks, Request, Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud, models
from app.api import dependencies
from app.exception.base_exception import category_not_found
from app.logger import logger

from app.schemas import CategoryCreate, CategoryDisplay, CategoryUpdate


router = APIRouter()


@router.get("/", response_model=List[CategoryDisplay])
async def get_categories(
    request: Request,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for getting all categories
    """
    categories = jsonable_encoder(crud.category.get_multi_without_limit(db_session))

    return categories


@router.post("/create", response_model=CategoryDisplay)
async def create_category(
    request: Request,
    category_in: CategoryCreate,
    db_session: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    """
    API for creating a new category
    """

    category = jsonable_encoder(crud.category.create(db_session, obj_in=category_in))

    return category


@router.patch("/update", response_model=CategoryDisplay)
async def update_category(
    request: Request,
    category_in: CategoryUpdate,
    db_session: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    """
    API for updating a category
    """

    db_obj = crud.category.get(db_session, id_value=category_in.id)

    if not db_obj:
        logger.error("Category with id %s not found", category_in.id)
        return category_not_found

    category = jsonable_encoder(
        crud.category.update(db_session, db_obj=db_obj, obj_in=category_in)
    )

    return category


@router.delete("/delete/{id}", response_model=CategoryDisplay)
async def delete_category(
    request: Request,
    id: int,
    db_session: Session = Depends(dependencies.get_db),
    current_user: models.User = Depends(dependencies.get_current_user),
):
    """
    API for deleting a category
    """

    category = crud.category.get(db_session, id_value=id)

    if not category:
        logger.error("Category with id %s not found", id)
        raise category_not_found

    category = jsonable_encoder(crud.category.remove(db_session, id=id))

    return category


@router.get("/search", response_model=List[CategoryDisplay])
async def search_category(
    request: Request,
    keyword: str,
    db_session: Session = Depends(dependencies.get_db),
):
    """
    API for searching categories
    """

    categories = jsonable_encoder(crud.category.search(db_session, keyword=keyword))

    return categories
