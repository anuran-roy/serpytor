from functools import lru_cache, wraps
from typing import Optional, Any, List, Dict, Tuple, Callable
import multiprocessing as mp
import threading as mt
import aiohttp
import asyncio
from queue import Queue, PriorityQueue

from serpytor.components.utils.algorithms.allocation.base_allocation import (
    BaseAllocation,
)


class Gateway:
    """
    The Gateway object aggregates the services by abstracting server details, and providing uniform APIs.

    Each gateway performs a set of logically-connected tasks across the servers. Each Gateway executes a specific task specified by its entrypoint during initialization.
    Gateway objects can be superposed on other Gateway objects for handling complex use cases.

    The diagram below represents how the gateways behave:

    <img alt='Gateway behaviour' src='https://imgur.com/qxcZ3ep.png' />
    """

    def __init__(
        self,
        task: Callable[..., Any],
        allocation_algorithm: BaseAllocation,
        task_data: Tuple[List[Any], Dict[str, Any]] = ([], {}),
        heartbeat_addresses: List[str] = [],
        resource_addresses: List[str] = [],
        *args: List[Any],
        **kwargs: Dict[str, Any]
    ) -> None:
        self._heartbeat_addr: List[str] = heartbeat_addresses
        self._resource_addr: List[str] = resource_addresses
        self._task: Callable[..., Any] = task
        self._task_input: Tuple[List[Any], Dict[str, Any]] = task_data
        self._allocation_algorithm: BaseAllocation = allocation_algorithm

    def __str__(*args: List[Any], **kwargs: Dict[str, Any]) -> str:
        ...

    def __repr__(*args: List[Any], **kwargs: Dict[str, Any]) -> str:
        ...

    async def get_available_resources(
        self, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Any:
        report: Dict[str, Dict[str, Any]] = {addr: {} for addr in self._resource_addr}
        async with aiohttp.ClientSession(timeout=kwargs.get("timeout", 10)) as session:
            for resource_addr, heartbeat_addr in zip(
                self._resource_addr, self._heartbeat_addr
            ):
                async with session.get(heartbeat_addr) as resp:
                    report[resource_addr] = await resp.json()

        return report

    def allocate_resource(self, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        """Get report from webservers at any given time"""
        report: Any = asyncio.run(self.get_available_resources())
        optimal_resource: Any = self._allocation_algorithm.queue(
            report, selection_criteria=kwargs.get("selection_criteria", "cpu")
        )
        return optimal_resource

    def execute(self, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        resource_details = self.allocate_resource()


if __name__ == "__main__":
    from serpytor.components.utils.algorithms.allocation.fcfs_allocation import (
        FCFSAllocation,
    )
    from serpytor.components.utils.algorithms.allocation.round_robin_allocation import (
        RoundRobinAllocation,
    )

    # Create a gateway object
    gateway = Gateway(
        task=lambda _: print("Hello World!"),
        allocation_algorithm=FCFSAllocation(),
        resource_addresses=[
            "http://localhost:8100/exec",
            "http://localhost:8101/exec",
            "http://localhost:8102/exec",
            "http://localhost:8103/exec",
        ],
        heartbeat_addresses=[
            "http://localhost:5000/heartbeat",
            "http://localhost:5001/heartbeat",
            "http://localhost:5002/heartbeat",
            "http://localhost:5003/heartbeat",
        ],
    )

    # Execute the gateway
    gateway.execute()
