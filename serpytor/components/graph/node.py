from functools import wraps
from typing import Callable, Any, Literal, Optional, List, Dict, Union


class Node:
    def __init__(
        self,
        task: Optional[Callable[..., Any]],
        task_params: Optional[Dict[str, Any]] = {},
        **kwargs
    ) -> None:
        self.task: Callable[..., Any] = task
        self.task_meta: Dict[str, Any] = {
            "name": task.__name__,
            "doc": task.__doc__,
            "module": task.__module__,
            "file": task.__code__.co_filename,
        }
        self._task_params = task_params

    def set_task(self, task: Callable[..., Any]) -> None:
        self.task = task

    @property
    def task_params(self) -> Dict[str, Any]:
        return self._task_params

    def set_task_meta(self, task_meta: Dict[str, Any]) -> None:
        self.task_meta = task_meta

    def set_task_params(
        self,
        mode: Optional[Literal["overwrite", "append"]] = "append",
        **task_params: Dict[str, Any]
    ) -> None:
        self._task_params = (
            self._task_params | task_params if mode == "overwrite" else task_params
        )

    def execute_task(self, *args, **kwargs) -> Any:
        return self.task(self.task_params, *args, **kwargs)
