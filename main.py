import asyncio
import logging

from config import setup_logging, settings
from scraper import Scraper

logger = logging.getLogger(__name__)


async def main():
    """Entry point for the scraper job."""

    setup_logging()
    scraper = Scraper(settings.site_url, settings.site_name)

    try:
        await scraper.run()
    except KeyboardInterrupt:
        logger.warning("Scraping interrupted by user.")
    except Exception as e:
        logger.error("Fatal error during scraping: %s", e, exc_info=True)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Scraping interrupted by user")
