from typing import Any, Callable, Dict, Literal, Optional


class Node:
    """Represents the node in a distributed computational graph."""

    def __init__(
        self,
        task: Optional[Callable[..., Any]],
        task_params: Optional[Dict[str, Any]] = {},
        **kwargs
    ) -> None:
        self._task: Callable[..., Any] = task
        self._task_meta: Dict[str, Any] = {
            "name": self._task.__name__,
            "doc": self._task.__doc__,
            "module": self._task.__module__,
            # "file": self._task.__code__.co_filename,
            "cellvars": self._task.__code__.co_cellvars,
            "stack_size": self._task.__code__.co_stacksize,
        }
        self._task_params = task_params

    def set_task(self, task: Callable[..., Any]) -> None:
        """Method to set the task callable after Node creation.
        **WARNING**: Not recommended to use unless you know what you're doing!
        """
        self._task = task

    @property
    def task(self):
        """Property that returns the task callable."""
        return self._task

    @property
    def task_params(self) -> Dict[str, Any]:
        """Property that returns the task params."""
        return self._task_params

    @property
    def task_meta(self) -> Dict[str, Any]:
        """Property that returns the task meta."""
        return self._task_meta

    def set_task_meta(self, task_meta: Dict[str, Any]) -> None:
        """Method to set the task metadata after Node creation.
        **WARNING**: Not recommended to use unless you know what you're doing!
        """
        self.task_meta = task_meta

    def set_task_params(
        self,
        mode: Optional[Literal["overwrite", "append"]] = "append",
        **task_params: Dict[str, Any]
    ) -> None:
        """Method to set the task params after Node creation.
        **WARNING**: Not recommended to use unless you know what you're doing!
        """
        self._task_params = (
            self._task_params | task_params if mode == "overwrite" else task_params
        )

    def execute_task(self, *args, **kwargs) -> Any:
        """Method to execute the callable attached to the Node.
        Executes callable along with set task params with (kw)args passed at runtime.
        """
        return self._task(self.task_params, *args, **kwargs)
