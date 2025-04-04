# logging_config.py
import logging
from logging.handlers import RotatingFileHandler
import os


def setup_logging():
    LOG_DIR = "logs"
    LOG_FILE = "app.log"
    os.makedirs(LOG_DIR, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = RotatingFileHandler(
            os.path.join(LOG_DIR, LOG_FILE), maxBytes=2_000_000, backupCount=5
        )
        formatter = logging.Formatter(
            "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        console = logging.StreamHandler()
        console.setFormatter(formatter)
        logger.addHandler(console)
