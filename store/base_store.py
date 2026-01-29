import logging
from typing import Iterable, List, Set, Dict, Any
from abc import ABC, abstractmethod

from scraper import Record

logger = logging.getLogger(__name__)


class BaseStore(ABC):
    """Abstract base class for persisting scraped records."""

    @abstractmethod
    def load_all_records(self) -> List[Dict[str, Any]]:
        """Load all existing records from the store."""
        pass

    @abstractmethod
    def save_records(self, records: Iterable[Record]) -> None:
        """Save a collection of scraped records to the store."""
        pass

    @abstractmethod
    def load_seen_ids(self) -> Set[str]:
        """Load the set of record IDs that have already been processed."""
        pass

    @abstractmethod
    def save_seen_ids(self, ids: Set[str]) -> None:
        """Save the set of seen record IDs to the store."""
        pass

    @abstractmethod
    def clear(self) -> None:
        """Clear all stored records."""
        pass
