from functools import cache
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


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
    docs_url: str = "/docs"
    redoc_url: str = "/redoc"
    routers: Routers = Routers()
    root_path: Optional[Literal["/prod", "/stage"]] = None


class Logger(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="logger_",
        case_sensitive=False,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    level: Literal["INFO", "DEBUG", "ERROR", "WARNING"] = "INFO"
    json_format: bool = False


class Settings(BaseSettings):
    logger: Logger = Logger()
    application: Application = Application()


@cache
def get_settings() -> Settings:
    return Settings()
