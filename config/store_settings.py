from pydantic import BaseModel
from pydantic_settings import BaseSettings


class JSONStoreConfig(BaseModel):
    """Configuration for JSON file storage backend."""
    data_dir: str = "data"
    records_filename_template: str = "{site_name}_dataset.json"
    seen_ids_filename_template: str = "{site_name}_seen_ids.json"


class StoreSettings(BaseSettings):
    """Storage backend configuration."""

    backend: str = "json"
    json_store: JSONStoreConfig = JSONStoreConfig()

    model_config = {
        "env_file": ".env"
    }


store_settings = StoreSettings()