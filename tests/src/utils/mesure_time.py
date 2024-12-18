import time
from functools import wraps
from typing import Callable

from tests.src.utils.logging import logger


def timeit(operation_name: str):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.monotonic()
            func(*args, **kwargs)
            duration = time.monotonic() - start_time
            logger.info("%s Duration: %.2f seconds", operation_name, duration)

        return wrapper

    return decorator
