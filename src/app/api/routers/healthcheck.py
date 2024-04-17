from fastapi import APIRouter, status

from app.core.logger import get_logger

router = APIRouter()


@router.get(
    "/healthcheck/",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def healthcheck() -> None:
    logger = get_logger()
    await logger.ainfo("Received healthcheck request")
