from typing import Any, List
from bs4 import BeautifulSoup
from vezilka_schemas import Record


class Parser:
    """Template class for parsing scraped data."""
    
    def __init__(self):
        pass

    def parse(self, raw_data: Any, metadata: Any = None) -> List[Record]:
        """Parse raw data into structured Record objects."""
        pass

    def _strip_html(self, raw_html: str) -> str:
        """Convert HTML content into plain text by removing tags and normalizing whitespace."""

        if not raw_html:
            return ""

        soup = BeautifulSoup(raw_html, "html.parser")
        text = soup.get_text(separator=" ", strip=True)

        return " ".join(text.split())
