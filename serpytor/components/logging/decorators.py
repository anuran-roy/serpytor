from functools import wraps
from typing import Any, Callable, List


def log(function: Callable, *args, **kwargs) -> Any:
    @wraps(function)
    def wrapper(*args: List, **kwargs):
        try:
            output = function(*args, **kwargs)
            return output
        except Exception:
            ...
