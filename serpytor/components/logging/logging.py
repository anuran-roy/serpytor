from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple

from serpytor.components.database.db import DBIO

# import logging
# import json
from .exceptions import CriticalLog, DebugLog, ErrorLog, InfoLog, UnknownLog, WarningLog

LOG_LEVELS: Dict[str, int] = {
    "UNKNOWN": 6,
    "CRITICAL": 5,
    "ERROR": 4,
    "WARNING": 3,
    "INFO": 2,
    "DEBUG": 1,
}


class DebugLogger:
    """
    Generate logs at the console.
    """

    def __init__(self, debug: bool = False, *args, **kwargs) -> None:
        self.log_dict: Dict[str, str] = {
            "UNKNOWN": "bold gray",
            "CRITICAL": "bold purple",
            "ERROR": "bold red",
            "WARNING": "bold yellow",
            "INFO": "bold green",
            "DEBUG": "bold white",
            "OTHER": "bold",
        }

    def log(self, function: Callable, *args, **kwargs) -> Any:
        """
        Log to console.
        """
        print("Passing through the StandardLogger log function")
        try:
            return function(*args, **kwargs)
        except Exception as e:
            print(f"\n{e}\n")


class StandardLogger:
    """
    Generate logs in time-series format to the database.
    """

    def __init__(
        self,
        db_url: str,
        log_threshold: Optional[int] = 3,
        debug: Optional[bool] = False,
        *args,
        **kwargs,
    ) -> None:
        self.log_dict: Dict[str, str] = {
            "UNKNOWN": "bold gray",
            "CRITICAL": "bold purple",
            "ERROR": "bold red",
            "WARNING": "bold yellow",
            "INFO": "bold green",
            "DEBUG": "bold white",
            "OTHER": "bold",
        }

        self.log_threshold = log_threshold
        self.db_url: str = db_url
        self.log_types: List[str] = list(self.log_dict.keys())
        self.table_name: str = kwargs.get("table_name", "logs")
        self.db_io: DBIO = DBIO(
            db_url=self.db_url, table_name=self.table_name, *args, **kwargs
        )

    def log(self, function: Callable, *args, **kwargs) -> Any:
        """
        Log to DB.
        """
        print("Passing through the StandardLogger log function")
        try:
            output: Any = function(*args, **kwargs)
            return output
        except Exception as logging_exception:
            self.log_index: Tuple[bool] = (
                isinstance(logging_exception, UnknownLog),
                isinstance(logging_exception, CriticalLog),
                isinstance(logging_exception, ErrorLog),
                isinstance(logging_exception, WarningLog),
                isinstance(logging_exception, InfoLog),
                isinstance(logging_exception, DebugLog),
                isinstance(logging_exception, Exception),
            )
            # print(f"\n\n\n\n{self.log_index}\n\n\n\n")
            # TODO: Log to DB.
            log: Dict[str, str] = {
                "timestamp": str(datetime.now()),
                "type": self.log_types[self.log_index.index(True)],
                "log": str(logging_exception),
            }
            print(f"Generated log details = \n{log}")
            if self.log_index.index(True) == len(self.log_types) - 1 or (
                (self.log_index.index(True) != len(self.log_types) - 1)
                and logging_exception.level >= self.log_threshold
            ):
                print(f"Writing exception {logging_exception}")
                self.db_io.write_to_db(log)
