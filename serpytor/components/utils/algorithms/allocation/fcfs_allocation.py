from typing import Any, Dict, Iterable, List, Union

from serpytor.components.utils.algorithms.allocation.base_allocation import (
    BaseAllocation,
)


class FCFSAllocation(BaseAllocation):
    """FCFS Allocation algorithm."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_queue()

    def __str__(self):
        return f"{self.__class__.__name__} algorithm.({len(self.queue_silo)} queues)"

    def queue(self, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        super().queue(*args, **kwargs)
        if len(self.queue_silo) == 0:
            raise ValueError("No queues found.")
        print("Returning queue at index 0.")
        return self.queue_silo[0].get(0)

    def put(self, item: Union[Iterable[Any], int, str, Any], index: int = 0) -> None:
        super().put(item, index=0)


if __name__ == "__main__":
    queue_ob = FCFSAllocation()
    queue_ob.put(index=0, item=[6, 1, 5, 4, 2, 3])

    for i in queue_ob.queue_silo:
        print(i)
