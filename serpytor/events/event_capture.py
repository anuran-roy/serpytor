from functools import wraps
from typing import Optional, Callable, List, Dict, Any
from serpytor.logging.logging import StandardLogger
# from serpytor.logging.decorators import 

class EventCapture:
    """
    Class-based handler for event capture with logging.
    """

    def __init__(
        self,
        event_name: Optional[str] = "Untitle Event Capture",
        logger: Optional[Callable] = StandardLogger("./db.json"),
        *args: Optional[List[Any]],
        **kwargs: Optional[Dict[str, Any]]
    ) -> None:
        self.db_url = kwargs.get("db_url")
        self.event_name = event_name
        self.logger = logger(*args, **kwargs)

    @self.logger.log
    def capture_event(self, function: Callable) -> None:
        @wraps
        def wrapper(*args, **kwargs):
            output = function()
        
            return output

        return wrapper

if __name__ == "__main__":
    ec = EventCapture()
    
    @ec.capture_event
    def hi():
        print("Hello")
    
    hi()