from typing import Any, Tuple, Callable
from functools import wraps
import logging
import json
from .exceptions import CriticalLog, ErrorLog, WarningLog, InfoLog, DebugLog


class DebugLogger:
    """
    Generate logs at the console.
    """

    def __init__(self, debug: bool = False, *args, **kwargs) -> None:
        self.log_types = {
            "WARNING": "bold yellow",
            "DEBUG": "bold white",
            "INFO": "bold green",
            "ERROR": "bold red",
            "CRITICAL": "bold purple",
        }

    def log(self, function: Callable, *args, **kwargs) -> Any:
        """
        Log to console.
        """

        @wraps
        def wrapper(*args: list, **kwargs: dict) -> None:
            try:
                output = function(*args, **kwargs)
                return output
            except Exception as e:
                print(f"\n{e}\n")

        return wrapper


class StandardLogger:
    """
    Generate logs in time-series format to the database.
    """

    def __init__(self, db_url: str, debug: bool = False, *args, **kwargs) -> None:
        self.log_types = {
            "WARNING": "bold yellow",
            "DEBUG": "bold white",
            "INFO": "bold green",
            "ERROR": "bold red",
            "CRITICAL": "bold purple",
        }

        self.db = db_url

    def log(self, function: Callable, *args, **kwargs) -> Any:
        """
        Log to DB.
        """

        @wraps
        def wrapper(*args: list, **kwargs: dict) -> None:
            try:
                output = function(*args, **kwargs)
                return output
            except Exception as e:
                self.log_types: Tuple[bool] = (
                    type(e) == type(CriticalLog),
                    type(e) == type(ErrorLog),
                    type(e) == type(WarningLog),
                    type(e) == type(InfoLog),
                    type(e) == type(DebugLog),
                )
                # TODO: Log to DB.

        return wrapper
