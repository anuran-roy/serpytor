import requests
import aiohttp
import asyncio
import time
from multiprocessing import Process
import os
from typing import List, Optional, Any, Dict, Union, Tuple, Callable
from datetime import datetime


# class HeartbeatClient:
#     def __init__(
#         self,
#         default_endpoint: Optional[str] = "http://172.16.25.252:6666",
#         time_interval: Optional[float] = 2.5,
#         *args: list,
#         **kwargs: dict,
#     ):
#         self.type = "Client"
#         self.time_interval: float = time_interval
#         self.default_endpoint: str = default_endpoint
#         self.heartbeat_started = None
#         self.heartbeat_stopped = None

#     def send_request(self, endpoint: Optional[str] = "") -> None:
#         if not endpoint:
#             endpoint = self.default_endpoint
#         print("Sending GET request to:", endpoint)
#         requests.get(endpoint)

#     def start_heartbeat(self) -> None:
#         try:
#             while True:
#                 self.send_request()
#                 time.sleep(self.time_interval)
#         except KeyboardInterrupt:
#             print("Shutting down client...")
#         except Exception as e:
#             print(f"Exception details: {e}")

#     async def heartbeat_controller(self, signal: Optional[str] = "start"):
#         self.heartbeat_process = Process(target=self.start_heartbeat)


class HeartbeatClient:
    """The HeartbeatClient component provides the necessary structure and functions to:
      
    1. Enwrap heartbeats across entrypoints.
    2. Define logging behaviours
    3. Run heartbeats independently in separate processes than entrypoint functions
    4. Set intervals independently for each type of heartbeat defined.
    5. Set separate destinations for each type of heartbeat defined.  
      
    Use HeartbeatClient to derive classes with appropriate heartbeat mechanisms.  
      
    Example usage:  
      
    ```python
    from serpytor.components.connection import HeartbeatClient
    
    class WrappedHeartbeatClient(HeartbeatClient):
        def __init__(self, destinations=[], entrypoint=None, *args, **kwargs):
            super(WrappedHeartbeatClient, self).__init__(
                destinations=destinations, entrypoint=entrypoint, *args, **kwargs
            )

        def log_action(self, e: Any) -> Any:
            print(f"Exception logged! Details: {e}")

    def test_method():
        print("Raising exception...")
        raise Exception("Random Exception")

    client = WrappedHeartbeatClient(
        destinations=[
            "http://localhost:5000",
            "http://localhost:5001",
            "http://localhost:5002",
            "http://localhost:5003",
        ],
        entrypoint=test_method,
        interval=5,
    )
    client.orchestrate_tasks()
    
    ```
    """

    def __init__(
        self,
        entrypoint: Optional[Callable] = None,
        destinations: Optional[Union[Tuple[str], List[str]]] = [],
        # os.getenv(
        #     "HEARTBEAT_DESTINATION"
        # ),
        *args: Optional[List[Any]],
        **kwargs: Optional[Dict[str, Any]],
    ):
        self.destinations: Union[Tuple[str], List[str]] = destinations
        self.node_name: str = kwargs.get("node_name", "Untitled Node")
        self.interval: float = kwargs.get("interval", 2.0)
        self.args: Union[Tuple[Any], List[Any]] = args
        self.location: str = __file__
        self.heartbeat_process: Process = None
        self.entrypoint: Callable = entrypoint
        self.entrypoint_args: Union[Tuple[Any], List[Any]] = kwargs.get(
            "entrypoint_args", []
        )
        self.entrypoint_kwargs: Dict[str, Any] = kwargs.get("entrypoint_kwargs", {})
        self.async_session = None

    def generate_heartbeat(self) -> Dict[str, Any]:
        return {
            "timestamp": str(datetime.now()),
            "node": self.node_name,
            "location": self.location,
        }

    # def link_heartbeat(self, ):
    #     ...

    async def send_heartbeat(self, session, destination: str) -> Any:

        async with session.post(destination) as resp:
            # print(f"Sending request to {destination}")
            ack = await resp.json(content_type="text/json")
            # print(ack)
            return ack

    async def orchestrate_requests(self):
        # print("Orchestrating requests...")
        self.async_session = aiohttp.ClientSession()
        async with self.async_session as session:
            tasks = []
            # print("Adding tasks...")

            for destination in self.destinations:
                # print(f"Sending request to {destination}...")
                tasks.append(
                    asyncio.ensure_future(self.send_heartbeat(session, destination))
                )

            completed_tasks = await asyncio.gather(*tasks)
            for task in completed_tasks:
                print("Task=", task)
        # print("Orchestrating complete...")

    def schedule_heartbeat(self):
        while True:
            # print("Starting one round of heartbeat scheduling...")
            asyncio.run(self.orchestrate_requests())
            asyncio.run(asyncio.sleep(self.interval))

    def wrap_entrypoint(self, entrypoint: Callable):
        self.entrypoint = entrypoint

    def log_action(self, e: Any) -> Any:
        ...

    def orchestrate_tasks(self):
        self.heartbeat_process = Process(target=self.schedule_heartbeat)
        self.entrypoint_process = Process(
            target=self.entrypoint,
            args=tuple(self.entrypoint_args),
            kwargs=self.entrypoint_kwargs,
        )

        try:
            self.entrypoint_process.start()
            self.heartbeat_process.start()
        except Exception as e:
            self.entrypoint_process.terminate()
            self.heartbeat_process.terminate()
            self.log_action(e)


if __name__ == "__main__":

    class WrappedHeartbeatClient(HeartbeatClient):
        def __init__(self, destinations=[], entrypoint=None, *args, **kwargs):
            super(WrappedHeartbeatClient, self).__init__(
                destinations=destinations, entrypoint=entrypoint, *args, **kwargs
            )

        def log_action(self, e: Any) -> Any:
            print(f"Exception logged! Details: {e}")

    def test_method():
        print("Raising exception...")
        raise Exception("Random Exception")

    client = WrappedHeartbeatClient(
        destinations=[
            "http://localhost:5000",
            # "http://localhost:5000",
            # "http://localhost:5000",
            # "http://localhost:5000",
        ],
        entrypoint=test_method,
        interval=5,
    )
    client.orchestrate_tasks()