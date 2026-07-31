import functools
import time
from src.logging_setup import get_logger

logger = get_logger("decorators")


def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"{func.__name__} took {elapsed*1000:.2f}ms")
        return result

    return wrapper
