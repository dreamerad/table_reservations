import datetime
import logging
import sys
from pathlib import Path
from typing import Optional

from loguru import logger


class InterceptHandler(logging.Handler):
    def emit(self, record: logging.LogRecord) -> None:
        try:
            level = logger.level(record.levelname).name
        except ValueError:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        logger.opt(depth=depth, exception=record.exc_info).log(
            level, record.getMessage()
        )


def setup_logging():
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    today = datetime.datetime.now().strftime("%Y-%m-%d")
    logger.remove()

    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO",
        colorize=True,
    )

    # Добавляем обработчик для вывода в файл с ротацией
    logger.add(
        f"logs/app_{today}.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="DEBUG",
        rotation="00:00",
        compression="zip",
        retention="30 days",
    )

    logger.add(
        "logs/errors.log",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
        level="ERROR",
        rotation="10 MB",
        compression="zip",
    )

    logging.basicConfig(handlers=[InterceptHandler()], level=0, force=True)
    for logger_name in logging.root.manager.loggerDict.keys():
        module_logger = logging.getLogger(logger_name)
        module_logger.handlers = [InterceptHandler()]
        module_logger.propagate = False

    logger.info("Logging system initialized")


def get_logger(name: Optional[str] = None):
    return logger.bind(name=name or "app")
