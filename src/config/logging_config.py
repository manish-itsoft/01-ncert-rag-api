# config/logging_config.py

import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime
from config.settings import settings

LOG_DIR = settings.log.DIR

os.makedirs(LOG_DIR, exist_ok=True)

def get_logger(name: str) -> logging.Logger:
    """
    Creates a module-specific logger with a rotating file handler.
    """

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent double handlers when re-importing
    if logger.handlers:
        return logger

    # Log formatting
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # log_filename = os.path.join(
    #     LOG_DIR,
    #     f"ingestion_{datetime.now().strftime('%Y-%m-%d')}.log"
    # )
    
    # # Rotating file handler
    # file_handler = RotatingFileHandler(
    #     log_filename,
    #     maxBytes=5 * 1024 * 1024,   # 5 MB
    #     backupCount=5
    # )
    # file_handler.setFormatter(formatter)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger