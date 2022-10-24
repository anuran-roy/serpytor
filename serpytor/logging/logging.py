from typing import Any, Tuple, Callable, Dict, Optional, List, Union, Iterable
from functools import wraps
import logging
import json
from .exceptions import CriticalLog, ErrorLog, WarningLog, InfoLog, DebugLog, UnknownLog
from tinydb import TinyDB, Query
from serpytor.config import CONFIG
from datetime import datetime
from serpytor.database.db import DBIO

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
        try:
            output = function(*args, **kwargs)
            return output
        except Exception as e:
            print(f"\n{e}\n")


class StandardLogger:
    """
    Generate logs in time-series format to the database.
    """

    def __init__(
        self,
        db_url: Optional[str] = CONFIG["TSDB"]["URL"],
        log_threshold: Optional[int] = 3,
        debug: Optional[bool] = False,
        *args,
        **kwargs,
    ) -> None:
        self.log_dict: Dict[str, str] = {
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
        self.table_name: str = kwargs.get("table_name", "_default")
        self.db_io: DBIO = DBIO(
            db_url=self.db_url, table_name=self.table_name, *args, **kwargs
        )

    def log(self, function: Callable, *args, **kwargs) -> Any:
        """
        Log to DB.
        """
        try:
            output: Any = function(*args, **kwargs)
            return output
        except Exception as e:
            self.log_index: Tuple[bool] = (
                type(e) == type(UnknownLog),
                type(e) == type(CriticalLog),
                type(e) == type(ErrorLog),
                type(e) == type(WarningLog),
                type(e) == type(InfoLog),
                type(e) == type(DebugLog),
                isinstance(e, Exception),
            )
            # TODO: Log to DB.
            log: Dict[str, str] = {
                "timestamp": str(datetime.now()),
                "type": self.log_types[self.log_index.index(True)],
                "log": str(e),
            }

            if self.log_index.index(True) == len(self.log_types) - 1 or (
                (self.log_index.index(True) != len(self.log_types) - 1)
                and e.level >= self.log_threshold
            ):
                print(f"Writing exception {e}")
                self.db_io.write_to_db(log)
