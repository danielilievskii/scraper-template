import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Set
from vezilka_schemas import Record

from .base_store import BaseStore

logger = logging.getLogger(__name__)


class JSONFileStore(BaseStore):
    """JSON file storage with separate files for records and IDs."""

    def __init__(self, records_file_path: str, seen_ids_file_path: str):
        self.records_file_path = Path(records_file_path)
        self.seen_ids_file_path = Path(seen_ids_file_path)

        self.records_file_path.parent.mkdir(parents=True, exist_ok=True)
        self.seen_ids_file_path.parent.mkdir(parents=True, exist_ok=True)

    def load_all_records(self) -> List[Dict[str, Any]]:
        """Load all records from the JSON file."""

        if not self.records_file_path.exists():
            return []

        try:
            with self.records_file_path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logger.warning("File %s is empty or corrupted. Returning empty list.", self.records_file_path)
            return []

    def save_records(self, records: List[Record]) -> None:
        """Append new records to the JSON file and update seen IDs."""

        if not records:
            logger.info("No records to save")
            return

        records_dicts = [record.to_dict() for record in records]

        existing_records = self.load_all_records()
        existing_records.extend(records_dicts)

        with self.records_file_path.open("w", encoding="utf-8") as f:
            json.dump(existing_records, f, indent=2, ensure_ascii=False)

        logger.info("Saved %d new records (total: %d)", len(records), len(existing_records))

        new_ids = {record.id for record in records}
        self.save_seen_ids(new_ids)

    def load_seen_ids(self) -> Set[str]:
        """Load the set of seen record IDs from the seen IDs file."""

        if not self.seen_ids_file_path.exists():
            return set()

        try:
            with self.seen_ids_file_path.open("r", encoding="utf-8") as f:
                ids_list = json.load(f)
                logger.info("Loaded %d previously seen IDs", len(ids_list))
                return set(ids_list)

        except json.JSONDecodeError:
            logger.warning("File %s is empty or corrupted. Returning empty set.", self.seen_ids_file_path)
            return set()

    def save_seen_ids(self, ids: Set[str]) -> None:
        """Append new IDs to the existing seen IDs file."""

        existing_ids = self.load_seen_ids()
        existing_ids.update(ids)

        with self.seen_ids_file_path.open("w", encoding="utf-8") as f:
            json.dump(sorted(list(existing_ids)), f, indent=2, ensure_ascii=False)

        logger.info("Added %d new IDs (total: %d)", len(ids), len(existing_ids))

    def clear(self) -> None:
        """Clear all stored records and seen IDs by deleting both files."""

        if self.records_file_path.exists():
            self.records_file_path.unlink()
            logger.info("Cleared records file: %s", self.records_file_path)

        if self.seen_ids_file_path.exists():
            self.seen_ids_file_path.unlink()
            logger.info("Cleared seen IDs file: %s", self.seen_ids_file_path)
