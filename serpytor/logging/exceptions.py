from datetime import datetime
from typing import Optional


class BaseLog(Exception):
    def __init__(self, message: Optional[str] = "An unknown error occurred.") -> None:
        self.message: str = message
        self.type: str = ""

    def __str__(self) -> str:
        return f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {self.type}: {self.message}"


class CriticalLog(BaseLog):
    def __init__(self, message: Optional[str] = "") -> None:
        super(self, BaseLog).__init__()
        self.message: str = message
        self.type: str = "CRITICAL"


class ErrorLog(BaseLog):
    def __init__(self, message: Optional[str] = "") -> None:
        super(self, BaseLog).__init__()
        self.message: str = message
        self.type: str = "FAULT"


class WarningLog(BaseLog):
    def __init__(self, message: Optional[str] = "") -> None:
        super(self, BaseLog).__init__()
        self.message: str = message
        self.type: str = "WARNING"


class InfoLog(BaseLog):
    def __init__(self, message: str = "") -> None:
        super(self, BaseLog).__init__()
        self.message: str = message
        self.type: str = "INFO"


class DebugLog(BaseLog):
    def __init__(self, message: str = "") -> None:
        super(self, BaseLog).__init__()
        self.message: str = message
        self.type: str = "DEBUG"
