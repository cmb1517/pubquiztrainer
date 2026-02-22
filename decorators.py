import time
import random
from functools import wraps
from logger import setup_logger

logger = setup_logger("retry")

def retry(max_tries=3, initial_delay=2, backoff_factor=2):
    """
    Exponential backoff retry decorator.
    - max_tries: Total attempts (including first try)
    - initial_delay: Seconds to wait after first failure
    - backoff_factor: Multiplier for the delay (2 = double each time)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            tries = 0
            delay = initial_delay
            
            while tries < max_tries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    tries += 1
                    if tries == max_tries:
                        logger.error(f"'{func.__name__}' failed after {max_tries} attempts: {e}")
                        raise e
                    
                    # Add a little "jitter" (randomness) so multiple tasks don't sync up
                    jitter = random.uniform(0, 1)
                    sleep_time = delay + jitter
                    
                    logger.warning(
                        f"'{func.__name__}' failed (Attempt {tries}/{max_tries}). "
                        f"Retrying in {sleep_time:.1f}s... Error: {e}"
                    )
                    
                    time.sleep(sleep_time)
                    delay *= backoff_factor
            return None
        return wrapper
    return decorator