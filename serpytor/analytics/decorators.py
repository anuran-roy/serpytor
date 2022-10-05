from typing import Callable, Any
import time
from functools import lru_cache, wraps
from serpytor.events.event_capture import EventCapture


def get_execution_time(func: Callable) -> Any:
    @wraps(func)
    def wrapper(*args: list, **kwargs: dict) -> Any:
        start_time: float = time.time()

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
