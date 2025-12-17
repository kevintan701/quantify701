"""
Utility functions for the quantitative trading system.
Includes logging setup, retry logic, and helper functions.
"""

import logging
import sys
from functools import wraps
from time import sleep
from typing import Callable, Any
import streamlit as st


def setup_logging():
    """
    Set up logging configuration for the application.
    Uses different levels based on environment.
    """
    # Check if we're in Streamlit environment
    in_streamlit = 'streamlit' in sys.modules
    
    # Configure logging
    log_level = logging.INFO if in_streamlit else logging.DEBUG
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=log_level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    # Reduce noise from third-party libraries
    logging.getLogger('yfinance').setLevel(logging.WARNING)
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    
    return logging.getLogger(__name__)


def retry_on_failure(max_attempts: int = 3, delay: float = 1.0, backoff: float = 2.0):
    """
    Decorator to retry a function on failure with exponential backoff.
    
    Args:
        max_attempts: Maximum number of retry attempts
        delay: Initial delay between retries in seconds
        backoff: Multiplier for delay after each retry
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            logger = logging.getLogger(__name__)
            last_exception = None
            current_delay = delay
            
            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_attempts - 1:
                        logger.warning(
                            f"{func.__name__} failed (attempt {attempt + 1}/{max_attempts}): {str(e)}. "
                            f"Retrying in {current_delay:.1f}s..."
                        )
                        sleep(current_delay)
                        current_delay *= backoff
                    else:
                        logger.error(
                            f"{func.__name__} failed after {max_attempts} attempts: {str(e)}"
                        )
            
            # If all retries failed, raise the last exception
            raise last_exception
        
        return wrapper
    return decorator


def rate_limit(max_calls_per_minute: int = 60):
    """
    Decorator to rate limit function calls.
    
    Args:
        max_calls_per_minute: Maximum number of calls allowed per minute
    """
    from time import time
    from collections import deque
    
    calls = deque()
    min_interval = 60.0 / max_calls_per_minute
    
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            now = time()
            
            # Remove calls older than 1 minute
            while calls and now - calls[0] > 60:
                calls.popleft()
            
            # If we're at the limit, wait
            if len(calls) >= max_calls_per_minute:
                sleep_time = min_interval - (now - calls[0])
                if sleep_time > 0:
                    sleep(sleep_time)
                    now = time()
                    # Clean up again after waiting
                    while calls and now - calls[0] > 60:
                        calls.popleft()
            
            # Record this call
            calls.append(now)
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

