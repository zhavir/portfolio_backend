from fastapi import FastAPI

from app.api.api_router import get_api_router
from app.core.settings import get_settings


def get_application() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        root_path=settings.application.root_path,  # type: ignore
        title=settings.application.title,
        version=settings.application.version,
    )

    app.include_router(get_api_router(), prefix=settings.application.routers.api_v1)

    return app


app = get_application()
