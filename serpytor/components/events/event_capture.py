from functools import wraps
from typing import Optional, Callable, List, Dict, Any
from serpytor.components.logging.logging import StandardLogger
from serpytor.components.analytics.decorators import get_execution_time

# from time import time

# from serpytor.components.logging.decorators import


class EventCapture:
    """
    Class-based handler for event capture with logging.
    """

    def __init__(
        self,
        db_url: str,
        event_name: Optional[str] = "Untitled Event Capture",
        logger: Optional[Callable] = StandardLogger,
        *args: Optional[List[Any]],
        **kwargs: Optional[Dict[str, Any]]
    ) -> None:
        self.db_url = db_url
        self.event_name = event_name
        self.logger = logger(db_url, *args, **kwargs)

    # @get_execution_time
    def capture_event(self, function: Callable) -> None:
        @wraps(function)
        def wrapper(*args, **kwargs):
            print("Passint through the event capture function")
            output = self.logger.log(function, *args, **kwargs)
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
