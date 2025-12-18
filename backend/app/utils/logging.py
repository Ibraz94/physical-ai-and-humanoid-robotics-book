import logging
import sys
from typing import Optional

def setup_logging(level: Optional[str] = None) -> None:
    """
    Set up logging configuration for the application
    """
    log_level = getattr(logging, level or "INFO")

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Create console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    # Add handler if not already added
    if not root_logger.handlers:
        root_logger.addHandler(console_handler)

def get_logger(name: str) -> logging.Logger:
    """
    Get a logger with the specified name
    """
    return logging.getLogger(name)