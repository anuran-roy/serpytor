from typing import Callable, Any
import time
from functools import lru_cache, wraps
# from serpytor.events.event_capture import EventCapture
from serpytor.config import CONFIG_ENV_VARS

def get_execution_time(func: Callable) -> Any:
    """Decorator to get execution time for a task/function/job.  
      
    Example usage:  
    ```
    from serpytor.analytics.decorators import get_execution_time
    @get_execution_time
    def foo():
        return "bar"
    ```
    """
    @wraps(func)
    def wrapper(*args: list, **kwargs: dict) -> Any:
        start_time: float = time.time()
        print("Passing through the get_execution_time function")
        output: Any = func(*args, **kwargs)

        end_time: float = time.time()
        execution_time: float = end_time - start_time

        # TODO: Add the execution time to the EventCapture instance.
        print(f"Execution time = {execution_time}s")
        return output

    return wrapper


if __name__ == "__main__":

    @get_execution_time
    def sample() -> None:
        time.sleep(2)

    sample()
