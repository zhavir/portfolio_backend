from functools import cache

from fastapi import APIRouter

from app.api.routers import email, healthcheck


@cache
def get_api_router() -> APIRouter:
    api_router = APIRouter()
    api_router.include_router(email.router, tags=["login"])
    api_router.include_router(healthcheck.router, tags=["healthcheck"])

    return api_router
