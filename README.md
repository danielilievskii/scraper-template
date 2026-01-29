# Scraper Template

An extensible template for building web scrapers that run as cron jobs. Clone this template and modify the classes directly to implement your scraper.

## Features

- Modular architecture with separate fetching, parsing, and storage

- Async-first design with built-in retry and rate-limiting

- Configurable logging to console and files

- Pluggable storage backend with duplicate detection

## Project Structure

```
scraper-template/
├── .github/
│   └── workflows/
│       └── daily-scraper.yml # GitHub Actions workflow to run the scraper and upload logs daily
├── config/
│   ├── logging.py            # Logging setup
│   ├── scraper_settings.py   # Scraper-specific settings
│   └── store_settings.py     # Storage-specific settings
├── scraper/
│   ├── fetcher.py       # Fetcher - template class for fetching data
│   ├── parser.py        # Parser - template class for parsing data
│   ├── scraper.py       # Scraper - main scraper orchestration
│   ├── models.py        # Record data model
├── store/
│   ├── base_store.py    # Base Storage class
│   ├── factory.py       # Store factory for dynamic backend selection
│   └── json_store.py    # JSON-based storage implementation
├── utils/
│   ├── rate_limiter.py  # Utilities for rate limiting
│   └── retry.py         # Utilities for retrying failed operations
├── main.py              # Entry point
└── requirements.txt     # Python dependencies
```

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Implement Your Scraper

Modify the template classes directly in their respective files:

- Edit `store/fetcher.py` and implement `fetch_metadata()` and `fetch_all()`
- Edit `store/parser.py` and implement `parse()`
- Edit or add a new store implementation in `store/` by extending BaseStore (the default JSONFileStore is already implemented).

### 3. Scraper Settings

Update `scraper_settings.py` with your details:

```python
from pydantic_settings import BaseSettings

class ScraperSettings(BaseSettings):

    ...
    site_url: str = "https://www.example.com"
    site_name: str = "example"
    ...
```

## Core Components

### Fetcher (`store/fetcher.py`)

Template class for fetching raw data from websites. Implement:
- `fetch_metadata()`: Fetch optional metadata (categories, pagination, etc.)
- `fetch_all()`: Fetch all raw data

### Parser (`scraper/parser.py`)

Template class for converting raw data into structured Record objects. Implement:
- `parse()`: Parse raw data into list of Record objects

Includes helper method:
- `strip_html()`: Convert HTML to plain text (already implemented)

### Store

The Store layer is responsible for persisting scraped records and tracking already-seen IDs to avoid duplicates.

#### BaseStore (`store/base_store.py`)

BaseStore defines the required interface:

- `load_all_records()`: Save new items
- `save_records(records)`: Load all stored items
- `load_seen_ids()`: Load IDs of already-processed records
- `save_seen_ids(ids)`: Save new seen IDs
- `clear()`: Remove all stored data

#### Store Factory (`store/factory.py`)

StoreFactory selects the storage backend based on configuration. Currently, only a JSON file backend is implemented.

#### JSONFileStore (`store/json_store.py`)

JSONFileStore stores (already implemented):

- Records in one JSON file

- Seen IDs in a separate JSON file

### Scraper (`scraper/scraper.py`)

The Scraper class orchestrates the full scraping workflow for a single website. It connects the fetcher, parser, and storage layers and runs them in a fixed pipeline.

The `run()` method performs:
1. Load previously seen IDs
2. Fetch metadata
3. Fetch raw data (skipping seen IDs)
4. Parse data
5. Save only new data

## Record Model

Scraped items are represented as Record objects with the following structure:

```python
{
    "id": "unique-identifier",        # Required: unique ID
    "title": "Record Title",         # Required
    "site_url": "https://site.com",   # Required: base site URL
    "page_url": "https://site.com/article",  # Required: full record URL
    "content": "Record content",     # Optional
    "published_at": "2024-01-01",     # Optional: ISO format datetime
    "categories": ["News", "Tech"]    # Optional
}
```

## Utilities

### Error Handling & Retries (`utils/retry.py`)

The template includes utilities for robust error handling:

```python
from utils import retry_on_exception


@retry_on_exception(max_retries=3, delay=1.0, backoff=2.0)
async def fetch_data():
    # Your fetching code
    pass
```

### Rate Limiting (`utils/rate_limiter.py`)

Control request frequency to be respectful to websites:

```python
from utils import RateLimiter

rate_limiter = RateLimiter(requests_per_second=1.0)


async def fetch_page(url):
    await rate_limiter.wait()  # Respect rate limit
    # Make request
```

## Configuration

Configuration is handled via environment variables and .env files using Pydantic settings. Default values are defined in the settings classes and can be overridden without changing code.

### Scraper Settings (`scraper_settings.py`)

Controls logging, site info, request behavior, rate limiting, retries, and headers. Logging is configured via utils/logging.py and respects these settings:

- `log_level`: Logging level (INFO, DEBUG, etc.)

- `log_format`: Format of log messages

- `log_to_file`: Enable writing logs to a file

- `log_file_path`: Path to the log file

### Storage Settings (`store_settings.py`)

Controls how and where scraped data is stored.

### Example `.env` overrides

```python
SITE_URL=https://news.yoursite.com
SITE_NAME=yoursite
LOG_LEVEL=DEBUG
REQUESTS_PER_SECOND=2
DATABASE_URL=your_database_url
```

