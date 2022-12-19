"""
    ROUTER FILE
"""
from fastapi import APIRouter

from app.api.v1.endpoints import (
    users,
    login,
    category,
    tag,
    post,
)

api_router = APIRouter()

api_router.include_router(login.router, prefix="/login", tags=["Login"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
api_router.include_router(category.router, prefix="/category", tags=["Category"])
api_router.include_router(tag.router, prefix="/tag", tags=["Tag"])
api_router.include_router(post.router, prefix="/post", tags=["Post"])
