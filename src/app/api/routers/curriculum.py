from fastapi import APIRouter, status

from app.core.logger import get_logger
from app.core.settings import get_settings
from app.models import Curriculum

router = APIRouter()


@router.post(
    "/curriculum/",
    status_code=status.HTTP_200_OK,
)
async def curriculum() -> Curriculum:
    logger = get_logger()
    settings = get_settings()
    await logger.ainfo("Received generate cv request")
    return Curriculum(download_link=settings.application.cv_download_link)
