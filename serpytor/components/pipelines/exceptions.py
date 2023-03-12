from serpytor.components.logging.exceptions import (CriticalLog, DebugLog,
                                                    ErrorLog, InfoLog,
                                                    WarningLog)


class CriticalPipelineError(CriticalLog):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class PipelineError(ErrorLog):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class PipelineWarning(WarningLog):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class PipelineInfo(InfoLog):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class PipelineDebugInfo(DebugLog):
    def __init__(self, message: str) -> None:
        super().__init__(message)
