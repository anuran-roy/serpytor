from functools import wraps
from typing import Optional, Callable, List, Dict, Any
from serpytor.logging.logging import StandardLogger
from time import time
from serpytor.config import CONFIG

# from serpytor.logging.decorators import
global LOGGER
LOGGER = StandardLogger


class EventCapture:
    """
    Class-based handler for event capture with logging.
    """

    def __init__(
        self,
        event_name: Optional[str] = "Untitled Event Capture",
        logger: Optional[Callable] = StandardLogger,
        db_url: Optional[str] = CONFIG["TSDB"]["URL"],
        *args: Optional[List[Any]],
        **kwargs: Optional[Dict[str, Any]]
    ) -> None:
        self.db_url = db_url
        self.event_name = event_name
        global LOGGER
        LOGGER = logger(db_url, *args, **kwargs)

    def capture_event(self, function: Callable) -> None:
        @wraps(function)
        def wrapper(*args, **kwargs):
            output = LOGGER.log(function, *args, **kwargs)
            # TODO: Other operations can be done here
            return output

        return wrapper


if __name__ == "__main__":
    ec = EventCapture()

    @ec.capture_event
    def hi():
        print("Hello")
        raise Exception("Random bs gooooooo!")

    hi()
