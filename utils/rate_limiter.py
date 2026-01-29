import asyncio


class RateLimiter:
    """Simple rate limiter to control request frequency."""

    def __init__(self, requests_per_second: float = 1.0):
        self.min_interval = 1.0 / requests_per_second if requests_per_second > 0 else 0
        self.last_request_time = 0.0
        self._lock = asyncio.Lock()

    async def wait(self) -> None:
        """Wait if necessary to respect rate limit."""

        if self.min_interval <= 0:
            return

        async with self._lock:
            current_time = asyncio.get_event_loop().time()
            time_since_last = current_time - self.last_request_time

            if time_since_last < self.min_interval:
                wait_time = self.min_interval - time_since_last
                await asyncio.sleep(wait_time)

            self.last_request_time = asyncio.get_event_loop().time()
