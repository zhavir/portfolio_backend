from functools import cache
from typing import Literal, Optional

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.constants import Environment


class Routers(BaseSettings):
    api_v1: str = "/api/v1"


class Application(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="application_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    title: str = "Portfolio API"
    version: str = "0.1.0"
    routers: Routers = Routers()
    environment: Optional[Environment] = None
    allow_origin: str = "http://localhost:3000"
    cv_download_link: str = "tmp/Cv.pdf"

    @computed_field  # type: ignore[misc]
    @property
    def root_path(self) -> str:
        if self.environment:
            return f"/{self.environment}"
        return ""


class Logger(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="logger_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    level: Literal["INFO", "DEBUG", "ERROR", "WARNING"] = "INFO"
    json_format: bool = True


class Aws(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="aws_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    email_topic_arn: str = "arn:aws:sns:us-east-1:000000000000:EmailTopic"
    endpoint: Optional[str] = None


class Settings(BaseSettings):
    logger: Logger = Logger()
    application: Application = Application()
    aws: Aws = Aws()


@cache
def get_settings() -> Settings:
    return Settings()
