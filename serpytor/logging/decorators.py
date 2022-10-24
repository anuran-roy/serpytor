from functools import wraps
from .exceptions import CriticalLog, ErrorLog, WarningLog, InfoLog, DebugLog
from typing import Optional, List, Any, Callable
from .logging import StandardLogger, DebugLogger


def log(function: Callable, *args, **kwargs) -> Any:
    @wraps(function)
    def wrapper(*args: List, **kwargs):
        try:
            output = function(*args, **kwargs)
            return output
        except:
            pass
