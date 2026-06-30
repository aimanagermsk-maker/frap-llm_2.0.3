import logging
import logging.config

from pydantic import BaseModel
import logging
import sys

def setup_logging(level=logging.INFO):
    """Настраивает логирование для всего приложения."""
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    # Устанавливаем уровень для наших модулей
    logging.getLogger("app.services.processor").setLevel(logging.DEBUG)
    logging.getLogger("app.services.kafka_client").setLevel(logging.DEBUG)
    logging.getLogger("app.routers").setLevel(logging.INFO)

    logger = logging.getLogger(__name__)
    logger.info(f"Logging configured with level: {logging.getLevelName(level)}")



LOG_FORMAT = "%(asctime)s %(levelname)s [%(name)s] %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"


class LoggingConfig(BaseModel):
    """Секция конфига с уровнями логирования."""

    app: str = "INFO"
    uvicorn: str = "INFO"
    uvicorn_access: str = "INFO"
    uvicorn_error: str = "INFO"


def build_logging_config(logging_config: LoggingConfig) -> dict:
    """Собирает dictConfig из секции logging yaml-конфига."""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "standard": {
                "format": LOG_FORMAT,
                "datefmt": LOG_DATE_FORMAT,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "standard",
                "stream": "ext://sys.stderr",
            },
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["console"],
                "level": logging_config.uvicorn,
                "propagate": False,
            },
            "uvicorn.error": {"level": logging_config.uvicorn_error},
            "uvicorn.access": {
                "handlers": ["console"],
                "level": logging_config.uvicorn_access,
                "propagate": False,
            },
            "app": {
                "handlers": ["console"],
                "level": logging_config.app,
                "propagate": False,
            },
        },
    }


def setup_logging(logging_config: LoggingConfig) -> dict:
    """Применяет уровни логирования из конфига."""
    config = build_logging_config(logging_config)
    logging.config.dictConfig(config)
    return config
