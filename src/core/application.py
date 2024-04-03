from fastapi import FastAPI
from fastapi.responses import RedirectResponse

from src.api.api_router import get_api_router
from src.core.settings import get_settings


def get_application() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.application.title,
        version=settings.application.version,
        docs_url=settings.application.docs_url,
        openapi_url=f"{settings.application.docs_url}/openapi.json",
        redoc_url=settings.application.redoc_url,
    )

    app.include_router(get_api_router(), prefix=settings.application.routers.api_v1)

    @app.get("/", include_in_schema=False)
    async def docs_redirect() -> RedirectResponse:
        return RedirectResponse(url=settings.application.docs_url)

    return app


app = get_application()
