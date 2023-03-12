import multiprocessing as mp
from queue import Queue
from typing import Any, Dict, Iterable, List, Optional, Union


class BaseAllocation:
    """Base class for implementing queuing methods."""

    def __init__(
        self,
        num_queues: Optional[int] = 5,
        max_size: Optional[int] = 0,
        *args: List[Any],
        **kwargs: Dict[str, Any],
    ) -> None:
        self.max_size = max_size
        self.queue_silo: List = [Queue(maxsize=max_size) for _ in range(num_queues)]
        self.lock = mp.Lock()
        self.sortable_fields = kwargs.get("sortable_fields")

    def __str__(self) -> str:
        return f"{self.__class__.__name__}({len(self.queue)} items)"

    def add_queue(self, max_size=0) -> None:
        self.lock.acquire()
        new_queue = Queue(maxsize=max_size)
        self.queue_silo.append(new_queue)
        self.lock.release()

    def put(
        self,
        item: Union[Iterable[Any], int, str, Any],
        # pop: Optional[bool] = True,
        index: Optional[int],
        *args: Optional[List[Any]],
        **kwargs: Optional[Dict[str, Any]],
    ) -> None:
        """Put an item in the queue."""
        self.lock.acquire()
        if hasattr(item, "__iter__"):
            for i in item:
                self.queue_silo[index].put_nowait(i)
        else:
            self.queue_silo[index].put_nowait(item)
        self.lock.release()

    def queue(
        self, *args: Optional[List[Any]], **kwargs: Optional[Dict[str, Any]]
    ) -> Any:
        """Process the incoming items (using a queue) and return the result."""
        ...

    # def put_to_queue(self):
    #     result: Any = self.queue()

    def peek(
        self,
        queue_index: Optional[int] = 0,
        lower_limit: Optional[Union[int, None]] = None,
        upper_limit: Optional[int] = 5,
    ) -> Iterable[Any]:
        """Peek at the items in the queue. Put limit = -1 to peek at all items in the queue."""
        k = lower_limit if (lower_limit > 0 and lower_limit != None) else 0
        for item in self.queue_silo[queue_index]:
            yield item
            k += 1
            if k != -1 and k == upper_limit:
                break
