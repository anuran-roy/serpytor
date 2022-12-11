from functools import lru_cache, wraps
from typing import Optional, Any, List, Dict, Tuple, Callable
import multiprocessing as mp
import threading as mt
import aiohttp
import asyncio
from queue import Queue, PriorityQueue


class Gateway:
    """
    The Gateway object aggregates the services by abstracting server details, and providing uniform APIs, regardless of server details.

    Each gateway performs a set of logically-connected tasks across the servers. Each Gateway executes a specific task specified by its entrypoint during initialization.
    Gateway objects can be superposed on other Gateway objects for handling complex use cases.

    The diagram below represents how the gateways behave:

    <img alt='Gateway behaviour' src='https://imgur.com/qxcZ3ep.png' />
    """

    def __init__(
        self,
        task: Callable[..., Any],
        task_data: Tuple[List[Any], Dict[str, Any]] = ([], {}),
        resource_addresses: List[str] = [],
        *args: List[Any],
        **kwargs: Dict[str, Any]
    ) -> None:
        self._resource_addr = resource_addresses
        self._task: Callable[..., Any] = task
        self._task_input: Tuple[List[Any], Dict[str, Any]] = task_data

    def __str__(*args: List[Any], **kwargs: Dict[str, Any]) -> str:
        ...

    def __repr__(*args: List[Any], **kwargs: Dict[str, Any]) -> str:
        ...

    async def get_available_resources(
        self, *args: List[Any], **kwargs: Dict[str, Any]
    ) -> Any:
        report: Dict[str, Dict[str, Any]] = {addr: {} for addr in self._resource_addr}
        async with aiohttp.ClientSession() as session:
            for addr in self._resource_addr:
                async with session.get(addr) as resp:
                    report[addr] = await resp.json()

        return report

    def allocate_resource(self, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        report: Any = asyncio.run(self.get_available_resources())

    def execute(self, *args: List[Any], **kwargs: Dict[str, Any]) -> Any:
        ...
