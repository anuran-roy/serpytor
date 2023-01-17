import asyncio
from typing import Any, Callable, Dict, List, Optional, Tuple

import aiohttp
import cloudpickle

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
        task_data: Optional[Tuple[List[Any], Dict[str, Any]]] = ([], {}),
        heartbeat_addresses: Optional[List[str]] = [],
        resource_addresses: Optional[List[str]] = [],
        *args: Optional[List[Any]],
        **kwargs: Optional[Dict[str, Any]],
    ) -> None:
        self._heartbeat_addr: List[str] = heartbeat_addresses
        self._resource_addr: List[str] = resource_addresses
        self._task: Callable[..., Any] = task
        self._task_input: Tuple[List[Any], Dict[str, Any]] = task_data
        self._allocation_algorithm: BaseAllocation = allocation_algorithm

    def __str__(
        self, *args: Optional[List[Any]], **kwargs: Optional[Dict[str, Any]]
    ) -> str:
        return f"Gateway({self._task.__name__}) with {len(self._resource_addr)} resources at {self._resource_addr} using {self._allocation_algorithm.__class__.__name__} algorithm"

    def __repr__(
        self, *args: Optional[List[Any]], **kwargs: Optional[Dict[str, Any]]
    ) -> str:
        return f"Gateway({self._task.__name__}) with {len(self._resource_addr)} resources at {self._resource_addr} using {self._allocation_algorithm.__class__.__name__} algorithm"

    async def get_available_resources(
        self, *args: Optional[List[Any]], **kwargs: Optional[Dict[str, Any]]
    ) -> Any:
        report: Dict[str, Dict[str, Any]] = {addr: {} for addr in self._resource_addr}
        async with aiohttp.ClientSession(
            conn_timeout=kwargs.get("timeout", 10.0)
        ) as session:
            for resource_addr, heartbeat_addr in zip(
                self._resource_addr, self._heartbeat_addr
            ):
                async with session.get(heartbeat_addr) as resp:
                    report[resource_addr] = await resp.json()

        return report

    def allocate_resource(
        self, *args: Optional[List[Any]], **kwargs: Optional[Dict[str, Any]]
    ) -> Any:
        """Get report from webservers at any given time"""
        report: Any = asyncio.run(self.get_available_resources())
        optimal_resource: Any = self._allocation_algorithm.queue(
            report, selection_criteria=kwargs.get("selection_criteria", "cpu")
        )
        return optimal_resource

    async def execute(
        self, *args: Optional[List[Any]], **kwargs: Optional[Dict[str, Any]]
    ) -> Any:
        resource_details = self.allocate_resource()
        task_pickle = cloudpickle.dumps(self._task)
        task_args, task_kwargs = self._task_input
        args_pickle = cloudpickle.dumps(task_args)
        kwargs_pickle = cloudpickle.dumps(task_kwargs)

        execution_loc: str = (
            f"{resource_details['location']}/{kwargs.get('execution_endpoint', 'exec')}"
        )
        async with aiohttp.ClientSession(execution_loc) as session:
            async with session.post(
                execution_loc,
                files={
                    "code": task_pickle,
                    "args": args_pickle,
                    "kwargs": kwargs_pickle,
                },
            ) as resp:
                return await resp.text()

        # Execute the task


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
