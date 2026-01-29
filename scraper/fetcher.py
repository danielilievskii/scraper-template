from typing import Any, Optional


class Fetcher:
    """Template class for fetching data from the site."""
    
    def __init__(self):
        pass
    
    async def fetch_metadata(self, *args, **kwargs) -> Optional[Any]:
        """Fetch any required metadata (e.g., categories, pagination info)."""
        pass

    async def fetch_data(self, *args, **kwargs) -> Any:
        """
        Fetch all raw data needed for scraping.
        This could be a list of JSON objects, HTML pages, etc.
        """
        pass
