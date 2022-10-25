from serpytor.components.logging.exceptions import (
    CriticalLog,
    ErrorLog,
    WarningLog,
    InfoLog,
    DebugLog,
)


class CriticalPipelineError(CriticalLog):
    def __init__(self, message: str) -> None:
        super(CriticalPipelineError, self).__init__(message)


class PipelineError(ErrorLog):
    def __init__(self, message: str) -> None:
        super(ErrorLog, self).__init__(message)


class PipelineWarning(WarningLog):
    def __init__(self, message: str) -> None:
        super(WarningLog, self).__init__(message)


class PipelineInfo(InfoLog):
    def __init__(self, message: str) -> None:
        super(InfoLog, self).__init__(message)


class PipelineDebugInfo(DebugLog):
    def __init__(self, message: str) -> None:
        super(DebugLog, self).__init__(message)
