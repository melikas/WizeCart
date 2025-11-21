"""Structured JSON logging setup for the assistant."""
import logging
import json
import sys
from pythonjsonlogger import jsonlogger
from real_time_shopping_assistant.config.settings import settings


def setup_logging():
    logger = logging.getLogger()
    level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    logger.setLevel(level)

    handler = logging.StreamHandler(sys.stdout)
    formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    handler.setFormatter(formatter)
    logger.handlers = [handler]

    return logger

logger = setup_logging()
