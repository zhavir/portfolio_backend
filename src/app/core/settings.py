from functools import cache
from typing import Literal

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
    environment: Environment = Environment.prod

    @computed_field  # type: ignore[misc]
    @property
    def root_path(self) -> str:
        return f"/{self.environment}"


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


class Settings(BaseSettings):
    logger: Logger = Logger()
    application: Application = Application()


@cache
def get_settings() -> Settings:
    return Settings()
