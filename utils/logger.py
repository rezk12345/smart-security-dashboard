"""Central logging configuration."""

import logging
from pathlib import Path

from utils.config import REPORT_DIR


def get_logger(name: str) -> logging.Logger:
    """Create or return a configured logger instance."""
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    log_path = Path(REPORT_DIR) / "security_dashboard.log"

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )

        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

    return logger
