from functools import wraps
from typing import Any, Callable, List, Optional

from .exceptions import CriticalLog, DebugLog, ErrorLog, InfoLog, WarningLog
from .logging import DebugLogger, StandardLogger


def log(function: Callable, *args, **kwargs) -> Any:
    @wraps(function)
    def wrapper(*args: List, **kwargs):
        try:
            output = function(*args, **kwargs)
            return output
        except:
            pass
