import logging
import sys
from functools import cache

import structlog

from app.core.settings import get_settings


@cache
def get_logger() -> structlog.stdlib.BoundLogger:
    settings = get_settings()

    logging.basicConfig(format="%(message)s", stream=sys.stdout, level=settings.logger.level)
    structlog.configure(
        processors=[
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )
    timestamper = structlog.processors.TimeStamper(fmt="%Y-%m-%d %H:%M:%S")
    formatter = structlog.stdlib.ProcessorFormatter(
        foreign_pre_chain=[
            structlog.stdlib.add_log_level,
            structlog.stdlib.ExtraAdder(),
            structlog.stdlib.add_logger_name,
            timestamper,
        ],
        processors=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.ProcessorFormatter.remove_processors_meta,
            timestamper,
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.format_exc_info,
            structlog.processors.EventRenamer("msg"),
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer() if settings.logger.json_format else structlog.dev.ConsoleRenderer(),  # type: ignore
        ],
    )

    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger = logging.getLogger()
    logger.handlers.clear()
    logger.addHandler(handler)
    logger.setLevel(settings.logger.level)
    app_logger: structlog.stdlib.BoundLogger = structlog.get_logger("FileTrackerApp")
    app_logger.info("Log level set to", logger_level=settings.logger.level)
    return app_logger
