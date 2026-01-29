import asyncio
import logging
from functools import wraps
from typing import Callable
from time import sleep

logger = logging.getLogger(__name__)


def retry_on_exception(
    max_retries: int = 3,
    delay: float = 1.0,
    backoff: float = 2.0,
    exceptions: tuple = (Exception,),
    log_errors: bool = True
):
    """
    Decorator to retry a function on exceptions with exponential backoff.
    
    :param max_retries: Maximum number of retry attempts
    :param delay: Initial delay between retries in seconds
    :param backoff: Multiplier for delay after each retry
    :param exceptions: Tuple of exceptions to catch and retry on
    :param log_errors: Whether to log retry attempts
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        if log_errors:
                            logger.warning(
                                f"{func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {e}. "
                                f"Retrying in {current_delay:.2f}s..."
                            )
                        await asyncio.sleep(current_delay)
                        current_delay *= backoff
                    else:
                        if log_errors:
                            logger.error(f"{func.__name__} failed after {max_retries + 1} attempts: {e}")
            
            raise last_exception
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            current_delay = delay
            last_exception = None
            
            for attempt in range(max_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
                    if attempt < max_retries:
                        if log_errors:
                            logger.warning(
                                f"{func.__name__} failed (attempt {attempt + 1}/{max_retries + 1}): {e}. "
                                f"Retrying in {current_delay:.2f}s..."
                            )
                        sleep(current_delay)
                        current_delay *= backoff
                    else:
                        if log_errors:
                            logger.error(f"{func.__name__} failed after {max_retries + 1} attempts: {e}")
            
            raise last_exception
        
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        return sync_wrapper
    
    return decorator
