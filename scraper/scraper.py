import logging

from .fetcher import Fetcher
from .parser import Parser
from store import StoreFactory

logger = logging.getLogger(__name__)


class Scraper:
    """Template class for orchestrating the scraping workflow for a single website"""

    def __init__(self, site_url: str, site_name: str):
        self.site_url = site_url
        self.site_name = site_name

        self._fetcher = Fetcher()
        self._parser = Parser()
        self._store = StoreFactory.create(self.site_name)

    async def run(self):
        """Execute the full scraping pipeline."""

        logger.info("=" * 80)
        logger.info("Starting scraper for %s", self.site_url)
        logger.info("=" * 80)

        logger.info("Loading previously seen IDs...")
        seen_ids = self._store.load_seen_ids()

        logger.info("Fetching metadata...")
        metadata = await self._fetcher.fetch_metadata()
        
        logger.info("Fetching raw data...")
        raw_data = await self._fetcher.fetch_data(seen_ids=seen_ids, metadata=metadata)
        
        logger.info("Parsing data...")
        parsed_records = self._parser.parse(raw_data, metadata=metadata)

        if parsed_records:
            logger.info("Saving new records...")
            self._store.save_records(parsed_records)
        else:
            logger.info("No new records to save")
        
        logger.info("=" * 80)
        logger.info("Scraping completed for %s", self.site_url)
        logger.info("=" * 80)
