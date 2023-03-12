import json
import multiprocessing as mp
import pickle
import time
from datetime import datetime
from multiprocessing import Process
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import psutil
from aiohttp import web
from rich import print as rich_print


class ForbiddenDeviceException(Exception):
    def __str__(self):
        return "The device is forbidden to access the server."


class HeartbeatServer:
    def __init__(
        self,
        heartbeat_protocol: Optional[str] = "http",
        heartbeat_port: Optional[int] = 8000,
        heartbeat_host: Optional[str] = "127.0.0.1",
        heartbeat_server_args: List = [],
        heartbeat_server_kwargs: Optional[Dict[str, Any]] = {},
        *args,
        **kwargs,
    ) -> None:
        """
        Initializes the HeartbeatServer class with the heartbeat_mappings.

        Format for mapping:

        ```json
        {
            "/endpoint1": {
                "type": "get",
                "mapped_method": helloworld,
            },
            "/endpoint2": {
                "type": "post",
                "mapped_method": helloworld_post,
            }
        }
        ```

        If an endpoint type is not specified, defaults to "get"
        """

        self.heartbeat_web_server = web.Application()
        self.heartbeat_protocol: str = heartbeat_protocol
        self.heartbeat_port: int = heartbeat_port
        self.heartbeat_host: str = heartbeat_host
        self.heartbeat_server_kwargs: Dict[str, Any] = heartbeat_server_kwargs
        self.heartbeat_server_args: List[Any] = heartbeat_server_args
        self.resource_online: bool = False

        self.heartbeat_handler: Dict[str, Dict[str, Union[str, Callable]]] = {
            "/heartbeat": {
                "type": "get",
                "mapped_method": lambda request: web.Response(
                    text=json.dumps(
                        {
                            "location": f"{self.heartbeat_protocol}://{self.heartbeat_host}:{self.heartbeat_port}",
                            "message": request.remote,
                            "cpu": psutil.cpu_percent(),
                            "memory": psutil.virtual_memory()[2],
                        }
                    )
                ),
            },
        }

        self.heartbeat_mappings: List[
            Tuple[str, Callable]
        ] = self.heartbeat_handler.items()

    def transform_mappings(
        self, mappings: Dict[str, Dict[str, Union[str, Callable]]]
    ) -> List[Callable]:
        transformed_heartbeat_mappings: List[Callable] = []

        for i in mappings:
            request_type = i[1].get("type", "get")

            if request_type == "get":
                transformed_heartbeat_mappings.append(
                    web.get(i[0], i[1]["mapped_method"])
                )
            elif request_type == "post":
                transformed_heartbeat_mappings.append(
                    web.post(i[0], i[1]["mapped_method"])
                )
            elif request_type == "put":
                transformed_heartbeat_mappings.append(
                    web.put(i[0], i[1]["mapped_method"])
                )
            elif request_type == "patch":
                transformed_heartbeat_mappings.append(
                    web.patch(i[0], i[1]["mapped_method"])
                )
            elif request_type == "delete":
                transformed_heartbeat_mappings.append(
                    web.delete(i[0], i[1]["mapped_method"])
                )

        return transformed_heartbeat_mappings

    def start_heartbeats(self) -> None:
        transformed_heartbeat_mappings = self.transform_mappings(
            self.heartbeat_mappings
        )
        self.heartbeat_web_server.add_routes(transformed_heartbeat_mappings)
        # try:
        heartbeat_process = Process(
            target=web.run_app,
            args=(*self.heartbeat_server_args,),
            kwargs={
                "print": None,
                "app": self.heartbeat_web_server,
                "port": self.heartbeat_port,
                "host": self.heartbeat_host,
                **self.heartbeat_server_kwargs,
            },
        )
        rich_print(
            f"[blue][+] Starting heartbeat server at {self.heartbeat_host}:{self.heartbeat_port}[/blue]"
        )
        self.resource_online = True
        heartbeat_process.start()
        # rich_print(
        #     f"Stopping heartbeat server at {self.heartbeat_host}:{self.heartbeat_port}"
        # )
        # heartbeat_process.join()
        # self.resource_online = False
        # except Exception as e:
        # rich_print(f"Server {self.__str__} crashed :(")
        # self.resource_online = False


class Server(HeartbeatServer):
    def __init__(
        self,
        mappings: Dict[str, Dict[str, Union[str, Callable]]],
        server_port: int,
        server_host: str,
        server_protocol: Optional[str] = "http",
        *args: List[Any],
        **kwargs: Dict[str, Any],
    ) -> None:
        super().__init__(*args, **kwargs)
        self.mappings: List[Tuple[str, Callable]] = mappings.items()
        self.service_web_server = web.Application()
        self.server_metadata: Dict[str, str] = {
            "name": kwargs.get("server_name", "SerPyTor Server"),
            "spawned_on": kwargs.get("spawned_on", str(datetime.now())),
        }
        self.server_port: int = server_port
        self.server_host: str = server_host
        self.server_protocol: str = server_protocol
        self.process_lock = mp.Lock()
        self.service_online: bool = True

        self.heartbeat_handler: Dict[str, Dict[str, Union[str, Callable]]] = {
            "/heartbeat": {
                "type": "get",
                "mapped_method": lambda request: web.Response(
                    text=json.dumps(
                        {
                            "location": f"{self.server_protocol}://{self.server_host}:{self.server_port}",
                            "message": request.remote,
                            "cpu": psutil.cpu_percent(),
                            "memory": psutil.virtual_memory()[2],
                        }
                    ),
                    content_type="application/json",
                ),
            },
        }

        self.heartbeat_mappings: List[
            Tuple[str, Callable]
        ] = self.heartbeat_handler.items()

    def __str__(self):
        return "Server"

    def add_mappings(
        self, mappings: Dict[str, Dict[str, Union[str, Callable]]]
    ) -> None:
        """Transforms the given endpoint definitions.
        This changes them to their respective route commands.
        This means less hassle to add endpoints to the web server
        """
        self.mappings.extend(mappings.items())

    def start_service(
        self,
        **server_kwargs,
    ) -> None:
        """Starts the service on the specified port and host.
        Uses a separate process to do the same so that a single error doesn't crash the entire server.
        """
        transformed_mappings: List[Callable] = self.transform_mappings(
            self.mappings)
        self.service_web_server.add_routes(transformed_mappings)

        try:
            p = Process(
                target=web.run_app,
                # args=(self.service_web_server),
                kwargs={
                    "print": None,
                    "app": self.service_web_server,
                    "port": self.server_port,
                    "host": self.server_host,
                    **server_kwargs,
                },
            )
            rich_print(
                f"[green][*] Starting service web server at {self.server_host}:{self.server_port}...[/green]"
            )
            self.service_online = True
            p.start()
        # rich_print(f"Exiting service web server at {self.server_host}:{self.server_port}...")
        # p.join()
        # self.service_online = False
        except Exception as e:
            rich_print(f"Service {self.__str__} crashed :(\n Reason: {e}")
            self.service_online = False

    def is_service_online(self) -> bool:
        return self.service_online

    def execute(self) -> None:
        try:
            heartbeat_process = Process(target=self.start_heartbeats)
            service_process = Process(target=self.start_service)
            heartbeat_process.start()
            service_process.start()
        except KeyboardInterrupt:
            rich_print(
                f"[yellow]Gracefully exiting server at {self.server_host}:{self.heartbeat_port}...[/yellow]"
            )

            service_process.join()
            heartbeat_process.join()


if __name__ == "__main__":
    # HeartbeatServer().execute()
    # rich_print(detect_ip())

    # async def handleGet(request):
    #     """Contains the mapping method that will rich_print the IP of the request origin.
    #     It also returns the cpu and memory usage of the system the server instance is running on.
    #     """
    #     rich_print(request.remote)
    #     return web.Response(
    #         text=json.dumps(
    #             {
    #                 "message": request.remote,
    #                 "cpu": psutil.cpu_percent(),
    #                 "memory": psutil.virtual_memory()[2],
    #             }
    #         ),
    #         content_type="application/json",
    #     )

    async def hello(request):
        rich_print("Hello!")
        return web.Response(
            text=json.dumps({"message": "Hello!", "target": request.remote}),
            content_type="application/json",
        )

    def sanity_check(code, args, kwargs):
        """Checks if the code is safe to execute.
        This is done by checking if the code is a function, and if the args and kwargs are of the correct type.
        """
        # return (
        #     isinstance(code, types.FunctionType)
        #     and isinstance(args, tuple)
        #     and isinstance(kwargs, dict)
        # )

        return True

    async def exec_func(
        request, sanity_checking: Callable[..., bool] = sanity_check
    ) -> Any:
        """Receives a chunk of code (complete with imports, etc), executes it, and returns an output."""
        reader = await request.multipart()
        code_field = await reader.next()
        code = await code_field.read()
        args_field = await reader.next()
        args = await args_field.read()
        kwargs_field = await reader.next()
        kwargs = await kwargs_field.read()

        check_complete: bool = sanity_checking(
            pickle.loads(code),
            pickle.loads(args),
            pickle.loads(kwargs),
        )

        print("Received kwargs = ", pickle.loads(kwargs))
        message: str = "Sanity check not passed."
        output: Union[Any, None] = None
        if check_complete:
            start_time = time.time()
            output = pickle.loads(code)(
                *pickle.loads(args), **pickle.loads(kwargs))
            stop_time = time.time()
            message = "Sanity check passed."
        rich_print(
            f"[green][+]Computation from {request.remote} completed in {(stop_time - start_time):.5f} second(s).[/green]"
        )
        return web.Response(
            text=json.dumps({"message": message, "output": output}),
            content_type="application/json",
        )

    # heartbeat_mapping: Dict[str, Dict[str, Union[str, Callable[..., Any]]]] = {
    #     "/heartbeat": {"type": "get", "mapped_method": handleGet}
    # }
    mapping: Dict[str, Dict[str, Union[str, Callable[..., Any]]]] = {
        "/hello": {"type": "get", "mapped_method": hello},
        "/exec": {"type": "post", "mapped_method": exec_func},
    }

    def test_example_v2():
        server1 = Server(
            # heartbeat_mappings=heartbeat_mapping,
            heartbeat_port=5000,
            mappings=mapping,
            server_host="127.0.0.1",
            server_port=8100,
        )
        # server1.start_heartbeats()
        server2 = Server(
            # heartbeat_mappings=heartbeat_mapping,
            heartbeat_port=5001,
            mappings=mapping,
            server_host="127.0.0.1",
            server_port=8101,
        )
        # server2.start_heartbeats()
        server3 = Server(
            # heartbeat_mappings=heartbeat_mapping,
            heartbeat_port=5002,
            mappings=mapping,
            server_host="127.0.0.1",
            server_port=8102,
        )
        # server3.start_heartbeats()
        server4 = Server(
            # heartbeat_mappings=heartbeat_mapping,
            heartbeat_port=5003,
            mappings=mapping,
            server_host="127.0.0.1",
            server_port=8103,
        )
        # server4.start_heartbeats()

        servers = [server1, server2, server3, server4]
        processes = []

        for idx, i in enumerate(servers):
            rich_print(f"Spawning server {idx+1}")
            processes.append(Process(target=i.execute))

        for i in processes:
            i.start()

        # server1.start_heartbeats()

    test_example_v2()
