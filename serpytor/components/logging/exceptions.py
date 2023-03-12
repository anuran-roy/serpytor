from datetime import datetime
from typing import Optional


class BaseLog(Exception):
    def __init__(self, message: Optional[str] = "An unknown error occurred.") -> None:
        self.message: str = message
        self.type: str = ""
        self.level = 0

    def __str__(self) -> str:
        return f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {self.type}: {self.message}"


class CriticalLog(BaseLog):
    def __init__(self, message: Optional[str] = "") -> None:
        super().__init__()
        self.message: str = message
        self.type: str = "CRITICAL"
        self.level = 5


class ErrorLog(BaseLog):
    def __init__(self, message: Optional[str] = "") -> None:
        super().__init__()
        self.message: str = message
        self.type: str = "FAULT"
        self.level = 4


class WarningLog(BaseLog):
    def __init__(self, message: Optional[str] = "") -> None:
        super().__init__()
        self.message: str = message
        self.type: str = "WARNING"
        self.level = 3


class InfoLog(BaseLog):
    def __init__(self, message: str = "") -> None:
        super().__init__()
        self.message: str = message
        self.type: str = "INFO"
        self.level = 2


class DebugLog(BaseLog):
    def __init__(self, message: str = "") -> None:
        super().__init__()
        self.message: str = message
        self.type: str = "DEBUG"
        self.level = 1


class UnknownLog(BaseLog):
    def __init__(self, message: str = "") -> None:
        super().__init__()
        self.message: str = message
        self.type: str = "UNKNOWN"
        self.level = 6
