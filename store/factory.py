from pathlib import Path
from config import store_settings
from . import BaseStore
from .json_store import JSONFileStore


class StoreFactory:
    """Factory for creating storage backend instances."""

    @staticmethod
    def create(site_name: str) -> BaseStore:
        """Create a store instance based on configured backend."""

        backend = store_settings.backend.lower()

        if backend == "json":
            return StoreFactory._create_json_store(site_name)
        else:
            raise ValueError(f"Unsupported store backend: {backend}")

    @staticmethod
    def _create_json_store(site_name: str) -> JSONFileStore:
        """Create a JSON file store with site-specific paths."""

        config = store_settings.json_store

        data_dir = Path(config.data_dir)
        data_dir.mkdir(parents=True, exist_ok=True)

        records_filename = config.records_filename_template.format(site_name=site_name)
        seen_ids_filename = config.seen_ids_filename_template.format(site_name=site_name)

        return JSONFileStore(
            records_file_path=str(data_dir / records_filename),
            seen_ids_file_path=str(data_dir / seen_ids_filename),
        )