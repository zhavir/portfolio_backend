from functools import cache

from fastapi import APIRouter

from src.api.routers import email


@cache
def get_api_router() -> APIRouter:
    api_router = APIRouter()
    api_router.include_router(email.router, tags=["login"])

    return api_router
