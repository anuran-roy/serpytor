from queue import Queue
from typing import Any, Dict, Iterable, List, Optional


class TasksQueue:
    """Queue incoming tasks using the plain old FCFS scheduling algorithm by default.
    You can also use a set of predefined algorithms (using a one of the famously known algorithms), or create custom algorithms of your own.
    """

    def __init__(
        self,
        queue: Iterable[Any],
        queue_maxsize: Optional[int] = 0,
        # algorithm: Optional[BaseAllocation] = FCFSAllocation,
        *args: List[Any],
        **kwargs: Dict[str, Any]
    ) -> None:
        self._task_queue: Queue = Queue(maxsize=queue_maxsize)
        self._queue = queue
        # self.algorithm = algorithm(
        #     kwargs.get("algorithm_args", []), kwargs.get("algorithm_kwargs", {})
        # )

    def put(
        self, item: Optional[Any], *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Iterable[Any]:
        if hasattr(item, "__iter__"):
            for i in item:
                self._queue.put_nowait(i)
        else:
            self._queue.put_nowait(item)

    def pop(self):
        return self._queue.get_nowait()
