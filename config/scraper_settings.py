from pydantic_settings import BaseSettings


class ScraperSettings(BaseSettings):

    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s %(levelname)s %(name)s | %(message)s"
    log_to_file: bool = True
    log_file_path: str = "logs/scraper.log"

    # Site details
    site_url: str = "https://www.example.com"
    site_name: str = "example"

    # Scraping settings
    max_concurrent_requests: int = 10
    request_timeout: int = 20

    # Rate limiting
    requests_per_second: float = 5

    # Retry settings
    max_retries: int = 3
    retry_delay: float = 1.0
    retry_backoff: float = 2.0

    # HTTP headers
    headers: dict = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }

    model_config = {
        "env_file": ".env"
    }


settings = ScraperSettings()