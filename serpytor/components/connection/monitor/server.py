import json
import multiprocessing as mp
from datetime import datetime
from multiprocessing import Process
from typing import Any, Callable, Dict, List, Optional, Tuple, Union
import psutil
from aiohttp import web

from serpytor.components.connection.monitor.utils import detect_ip


class ForbiddenDeviceException(Exception):
    def __str__(self):
        return "The device is forbidden to access the server."


# class HeartbeatServer:
#     def __init__(self, hostName: str = "0.0.0.0", port: int = 6666) -> None:
#         self.heartbeat_port: int = port
#         self.type = "Server"
#         self.heartbeat_hostName: str = hostName
#         self.app = web.Application()
#         self.config = safe_load(open("./monitor_config.yml", "r").read())
#         self.routes = [web.get("/", self.handleRequest)]

#     async def handleRequest(self, request: web.Request) -> web.Response:
#         # print(dir(request))
#         try:
#             self.check_source(request.remote)
#             print(request.remote)
#             return web.Response(text="Hello World")
#         except ForbiddenDeviceException:
#             print(f"Forbidden device request: {request.remote}")

#     def check_source(self, ip_address: str) -> None:
#         if not self.is_whitelisted(ip_address):
#             raise ForbiddenDeviceException

#     def add_all_routes(self) -> None:
#         self.app.add_routes(self.routes)

#     def is_whitelisted(self, ip_address: str) -> bool:
#         if (
#             self.config["devices"]["clients"]["allow"] == "*"
#             and ip_address not in self.config["devices"]["clients"]["disallow"]
#         ):
#             return True
#         return (
#             ip_address in self.config["devices"]["clients"]["allow"]
#             or ip_address not in self.config["devices"]["clients"]["disallow"]
#         )

#     def listen(self) -> None:
#         print(f"Server started http://{self.heartbeat_hostName}:{self.heartbeat_port}")
#         self.add_all_routes()
#         web.run_app(self.app, host=self.heartbeat_hostName, port=self.heartbeat_port)

#     def stop_server(self) -> None:
#         self.app.shutdown()
#         print("Server stopped.")

#     def execute(self) -> None:
#         try:
#             self.listen()
#         except KeyboardInterrupt:
#             print("Shutting down...")
#             self.stop_server()


class HeartbeatServer:
    def __init__(
        self,
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

        self.heartbeat_handler: Dict[str, Dict[str, Union[str, Callable]]] = {
            "/heartbeat": {
                "type": "get",
                "mapped_method": lambda request: web.Response(
                    text=json.dumps(
                        {
                            "location": f"http://{self.heartbeat_host}:{self.heartbeat_port}",
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
        self.heartbeat_web_server = web.Application()
        self.heartbeat_port: int = heartbeat_port
        self.heartbeat_host: str = heartbeat_host
        self.heartbeat_server_kwargs: Dict[str, Any] = heartbeat_server_kwargs
        self.heartbeat_server_args: List[Any] = heartbeat_server_args
        self.resource_online: bool = False

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
                "app": self.heartbeat_web_server,
                "port": self.heartbeat_port,
                "host": self.heartbeat_host,
                **self.heartbeat_server_kwargs,
            },
        )
        print(
            f"Starting heartbeat server at {self.heartbeat_host}:{self.heartbeat_port}"
        )
        self.resource_online = True
        heartbeat_process.start()
        # print(
        #     f"Stopping heartbeat server at {self.heartbeat_host}:{self.heartbeat_port}"
        # )
        # heartbeat_process.join()
        # self.resource_online = False
        # except Exception as e:
        # print(f"Server {self.__str__} crashed :(")
        # self.resource_online = False


class Server(HeartbeatServer):
    def __init__(
        self,
        mappings: Dict[str, Dict[str, Union[str, Callable]]],
        server_port: int,
        server_host: str,
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
        self.process_lock = mp.Lock()
        self.service_online: bool = True

        self.heartbeat_handler: Dict[str, Dict[str, Union[str, Callable]]] = {
            "/heartbeat": {
                "type": "get",
                "mapped_method": lambda request: web.Response(
                    text=json.dumps(
                        {
                            "location": f"http://{self.server_host}:{self.server_port}",
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
        transformed_mappings: List[Callable] = self.transform_mappings(self.mappings)
        self.service_web_server.add_routes(transformed_mappings)

        try:
            p = Process(
                target=web.run_app,
                # args=(self.service_web_server),
                kwargs={
                    "app": self.service_web_server,
                    "port": self.server_port,
                    "host": self.server_host,
                    **server_kwargs,
                },
            )
            print(
                f"Starting service web server at {self.server_host}:{self.server_port}..."
            )
            self.service_online = True
            p.start()
        # print(f"Exiting service web server at {self.server_host}:{self.server_port}...")
        # p.join()
        # self.service_online = False
        except Exception as e:
            print(f"Service {self.__str__} crashed :(")
            self.service_online = False

    def is_service_online(self) -> bool:
        return self.service_online

    def execute(self) -> None:
        heartbeat_process = Process(target=self.start_heartbeats)
        service_process = Process(target=self.start_service)
        heartbeat_process.start()
        service_process.start()


if __name__ == "__main__":
    # HeartbeatServer().execute()
    # print(detect_ip())

    # async def handleGet(request):
    #     """Contains the mapping method that will print the IP of the request origin.
    #     It also returns the cpu and memory usage of the system the server instance is running on.
    #     """
    #     print(request.remote)
    #     return web.Response(
    #         text=json.dumps(
    #             {
    #                 "message": request.remote,
    #                 "cpu": psutil.cpu_percent(),
    #                 "memory": psutil.virtual_memory()[2],
    #             }
    #         ),
    #         content_type="text/json",
    #     )

    async def hello(request):
        print("Hello!")
        return web.Response(
            text=json.dumps({"message": "Hello!", "target": request.remote}),
            content_type="text/json",
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
        import pickle

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
        message: str = "Sanity check not passed."
        output: Union[Any, None] = None
        if check_complete:
            output = pickle.loads(code)(*pickle.loads(args), **pickle.loads(kwargs))
            message = "Sanity check passed."
        print("Computation complete.")
        return web.Response(
            text=json.dumps({"message": message, "output": output}),
            content_type="text/json",
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
            print(f"Spawning server {idx+1}")
            processes.append(Process(target=i.execute))

        for i in processes:
            i.start()

        # server1.start_heartbeats()

    test_example_v2()
