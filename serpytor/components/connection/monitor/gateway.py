import asyncio
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple

import aiohttp
import cloudpickle
import requests

from serpytor.components.utils.algorithms.allocation.base_allocation import \
    BaseAllocation


class Gateway:
    """
    The Gateway object aggregates the services by abstracting server details and providing uniform APIs.

    Each gateway performs a set of logically-connected tasks across the servers.
    Each Gateway executes a specific task specified by its entrypoint during initialization.
    Gateway objects can be superposed on other Gateway objects for handling complex use cases.

    The diagram below represents how the gateways behave:

    <img alt='Gateway behavior' src='https://imgur.com/qxcZ3ep.png' />
    """

    def __init__(
        self,
        task: Callable[..., Any],
        allocation_algorithm: BaseAllocation,
        task_setup_data: Optional[Tuple[List[Any], Dict[str, Any]]] = ([], {}),
        heartbeat_addresses: Optional[List[str]] = [],
        resource_addresses: Optional[List[str]] = [],
        *args: Optional[List[Any]],
        **kwargs: Optional[Dict[str, Any]],
    ) -> None:
        self._heartbeat_addr: List[str] = heartbeat_addresses
        self._resource_addr: List[str] = resource_addresses
        self._task: Callable[..., Any] = task
        self._task_setup_input: Tuple[List[Any], Dict[str, Any]] = task_setup_data
        self._allocation_algorithm: BaseAllocation = allocation_algorithm

    def __str__(self) -> str:
        return f"Gateway({self._task.__name__}) with {len(self._resource_addr)} resources at {self._resource_addr} using {self._allocation_algorithm.__class__.__name__} algorithm"

    def __repr__(self) -> str:
        return f"Gateway({self._task.__name__}) with {len(self._resource_addr)} resources at {self._resource_addr} using {self._allocation_algorithm.__class__.__name__} algorithm"

    def set_task(self, task: Callable[..., Any]) -> None:
        self._task = task

    async def get_available_resources(
        self, *args: Optional[List[Any]], **kwargs: Optional[Dict[str, Any]]
    ) -> Any:
        """Get vitals report from webservers at any given time"""
        print("Getting available resources...")
        report: Dict[str, Dict[str, Any]] = {addr: {} for addr in self._resource_addr}
        async with aiohttp.ClientSession(
            # timeout=kwargs.get("timeout", 10.0)
        ) as session:
            print(f"Sending request to {len(self._resource_addr)} resources")
            for idx, zipped_tuple in enumerate(
                zip(self._resource_addr, self._heartbeat_addr)
            ):
                resource_addr, heartbeat_addr = zipped_tuple
                print(f"Sending request {idx+1}...")
                async with session.get(heartbeat_addr) as resp:
                    report[resource_addr] = await resp.json()

        return report

    async def allocate_resource(
        self, *args: Optional[List[Any]], **kwargs: Optional[Dict[str, Any]]
    ) -> Any:
        """Get vital reports from webservers at any given time."""
        report: Any = await self.get_available_resources()
        print("Received resource reports. Forwarding to allocation algorithm...")
        self._allocation_algorithm.put(report)
        optimal_resource: Any = self._allocation_algorithm.queue(
            selection_criteria=kwargs.get("selection_criteria", "cpu")
        )
        print(optimal_resource)
        return optimal_resource

    async def execute(
        self,
        task_return_type: Literal["batch", "stream"] = "batch",
        task_args: Optional[List[Any]] = [],
        task_kwargs: Optional[Dict[str, Any]] = {},
        *args: Optional[List[Any]],
        **kwargs: Optional[Dict[str, Any]],
    ) -> Any:
        """Execute the task on the allocated resource.
        We use sync requests here due to some problems with AIOHttp requests.
        Moreover, for a single request, sync requests are faster than async requests.
        """
        # while True:
        print("Task Kwargs received = ", task_kwargs)
        resource_details = await self.allocate_resource()
        task_pickle = cloudpickle.dumps(self._task)
        task_setup_args, task_setup_kwargs = self._task_setup_input
        args_pickle = cloudpickle.dumps(task_setup_args + task_args)
        print("Kwargs received at gateway = ", task_kwargs)
        kwargs_pickle = cloudpickle.dumps(task_setup_kwargs | task_kwargs)

        execution_loc: str = f"{resource_details}"

        print("Executing at", execution_loc)
        # Execute the task

        # async with aiohttp.ClientSession(execution_loc) as session:
        #     async with session.post(
        #         execution_loc,
        #         files={
        #             "code": task_pickle,
        #             "args": args_pickle,
        #             "kwargs": kwargs_pickle,
        #         },
        #     ) as resp:
        #         text = await resp.text()
        #         print(text)
        #         return text

        res = requests.post(
            execution_loc,
            files={
                "code": task_pickle,
                "args": args_pickle,
                "kwargs": kwargs_pickle,
            },
        )
        return res.json()


if __name__ == "__main__":
    import numpy as np

    from serpytor.components.utils.algorithms.allocation import FCFSAllocation

    # from serpytor.components.utils.algorithms.allocation import (
    #     RoundRobinAllocation,
    # )
    # Create a gateway object
    gateway = Gateway(
        task=lambda x: np.square(x).tolist(),
        task_setup_data=([], {}),
        allocation_algorithm=FCFSAllocation(),
        resource_addresses=[
            "http://127.0.0.1:8100/exec",
            "http://127.0.0.1:8101/exec",
            "http://127.0.0.1:8102/exec",
            "http://127.0.0.1:8103/exec",
        ],
        heartbeat_addresses=[
            "http://127.0.0.1:5000/heartbeat",
            "http://127.0.0.1:5001/heartbeat",
            "http://127.0.0.1:5002/heartbeat",
            "http://127.0.0.1:5003/heartbeat",
        ],
    )

    # Execute the gateway
    asyncio.run(
        gateway.execute(task_args=[np.random.randint(10, size=(10000, 10000)).tolist()])
    )
