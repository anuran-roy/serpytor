from functools import wraps
from typing import Any, Callable, Dict, List, Optional

from serpytor.components.logging.logging import StandardLogger

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
        """Wrapper function to capture an event.
        Triggered whenever the wrapped callable is called."""

        @wraps(function)
        def wrapper(*args, **kwargs):
            print("Passing through the event capture function")
            output = self.logger.log(function, *args, **kwargs)
            # TODO: Other operations can be done here
            return output

        return wrapper


if __name__ == "__main__":
    ec = EventCapture(db_url=":memory:")

    @ec.capture_event
    def hi():
        """Random function to test event capture mechanism"""
        print("Hello")
        raise Exception("Random bs gooooooo!")

    hi()
