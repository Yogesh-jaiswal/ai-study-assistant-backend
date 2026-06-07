import logging
import os

from flask import has_request_context, g
from logging.handlers import RotatingFileHandler

from configs import settings

class RequestIDFilter(logging.Filter):
    """Logging filter to add request ID to log records."""
    def filter(self, record):
        if has_request_context():
            record.request_id = getattr(g, "request_id", "unknown")
        else:
            record.request_id = "no-request"

        return True

def configure_logging():
    """Configure logging for the application."""

    if not os.path.exists("logs"): # Create logs directory if it doesn't exist
        os.makedirs("logs")

    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | [%(request_id)s] | %(message)s" # Log format with request ID
    )
    request_filter = RequestIDFilter()

    # Console handler for outputting logs to the console
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.addFilter(request_filter)

    # File handlers for app logs and error logs with rotation
    app_file_handler = RotatingFileHandler(
        "logs/app.log",
        maxBytes=1024*1024,
        backupCount=3
    )
    app_file_handler.setFormatter(formatter)
    app_file_handler.addFilter(request_filter)

    # Error file handler for logging errors separately
    error_file_handler = RotatingFileHandler(
        "logs/error.log",
        maxBytes=1024*1024,
        backupCount=3
    )
    error_file_handler.setLevel(logging.ERROR)
    error_file_handler.setFormatter(formatter)
    error_file_handler.addFilter(request_filter)

    # Configure the root logger
    root_logger = logging.getLogger()

    root_logger.setLevel(
        getattr(logging, settings.LOG_LEVEL)
    )

    # Add handlers to the root logger
    root_logger.addHandler(console_handler)
    root_logger.addHandler(app_file_handler)
    root_logger.addHandler(error_file_handler)