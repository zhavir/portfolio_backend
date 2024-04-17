from functools import cache

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.api_router import get_api_router
from app.core.boto_client_proxy import get_boto_client_proxy
from app.core.logger import get_logger
from app.core.settings import get_settings


@cache
def get_application() -> FastAPI:
    logger = get_logger()
    logger.info("Setup application")
    settings = get_settings()
    app = FastAPI(
        root_path=settings.application.root_path,
        title=settings.application.title,
        version=settings.application.version,
        boto_client_proxy=get_boto_client_proxy(),
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[settings.application.allow_origin],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(get_api_router(), prefix=settings.application.routers.api_v1)

    return app
