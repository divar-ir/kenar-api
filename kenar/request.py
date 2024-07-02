import time
from functools import wraps
from typing import Optional

import httpx


def retry(max_retries=3, delay=0):
    """
    Decorator for adding retry logic to functions making httpx requests.

    :param max_retries: Maximum number of retries.
    :param delay: Delay between retries in seconds.
    """

    def decorator_retry(func):
        @wraps(func)
        def wrapper_retry(*args, **kwargs):
            retries = 0
            response: Optional[httpx.Response] = None
            while True:
                try:
                    response = func(*args, **kwargs)
                    response.raise_for_status()
                    return response
                except httpx.HTTPStatusError as e:
                    retries += 1
                    if retries > max_retries:
                        error_details = response.text
                        raise Exception(
                            f"HTTP error occurred: {e}. Error Detail: {error_details}"
                        ) from None
                    time.sleep(delay)

        return wrapper_retry

    return decorator_retry
