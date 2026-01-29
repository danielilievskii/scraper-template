import logging
import sys
from pathlib import Path

from .scraper_settings import settings


def setup_logging() -> None:
    """Configure logging for the scraper based on settings.py."""

    handlers = [logging.StreamHandler(sys.stdout)]

    if settings.log_to_file:
        log_path = Path(settings.log_file_path)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        handlers.append(logging.FileHandler(settings.log_file_path))

    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format=settings.log_format,
        handlers=handlers,
    )
