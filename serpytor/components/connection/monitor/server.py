import aiohttp
from aiohttp import web
from yaml import safe_load
import time
import json
from datetime import datetime
from tinydb import TinyDB, Query
from serpytor.components.connection.monitor.utils import detect_ip
from typing import Optional, Callable, Tuple, Union, List, Dict, Any
from multiprocessing import Process


class ForbiddenDeviceException(Exception):
    def __str__(self):
        return "The device is forbidden to access the server."


class HeartbeatServer:
    def __init__(self, hostName: str = "0.0.0.0", port: int = 6666) -> None:
        self.port: int = port
        self.type = "Server"
        self.hostName: str = hostName
        self.app = web.Application()
        self.config = safe_load(open("./monitor_config.yml", "r").read())
        self.routes = [web.get("/", self.handleRequest)]

    async def handleRequest(self, request: web.Request) -> web.Response:
        # print(dir(request))
        try:
            self.check_source(request.remote)
            print(request.remote)
            return web.Response(text="Hello World")
        except ForbiddenDeviceException:
            print(f"Forbidden device request: {request.remote}")

    def check_source(self, ip_address: str) -> None:
        if not self.is_whitelisted(ip_address):
            raise ForbiddenDeviceException

    def add_all_routes(self) -> None:
        self.app.add_routes(self.routes)

    def is_whitelisted(self, ip_address: str) -> bool:
        if (
            self.config["devices"]["clients"]["allow"] == "*"
            and ip_address not in self.config["devices"]["clients"]["disallow"]
        ):
            return True
        return (
            ip_address in self.config["devices"]["clients"]["allow"]
            or ip_address not in self.config["devices"]["clients"]["disallow"]
        )

    def listen(self) -> None:
        print(f"Server started http://{self.hostName}:{self.port}")
        self.add_all_routes()
        web.run_app(self.app, host=self.hostName, port=self.port)

    def stop_server(self) -> None:
        self.app.shutdown()
        print("Server stopped.")

    def execute(self) -> None:
        try:
            self.listen()
        except KeyboardInterrupt:
            print("Shutting down...")
            self.stop_server()


class HeartbeatServerV2:
    def __init__(
        self,
        mappings: Dict[str, Dict[str, Union[str, Callable]]],
        port: Optional[int] = 8000,
        host: Optional[str] = "localhost",
        server_args: List = [],
        server_kwargs: Optional[Dict[str, Any]] = {},
        *args,
        **kwargs,
    ) -> None:
        """
        Initializes the HeartbeatServer class with the mappings.

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
        self.mappings: List[Tuple[str, Callable]] = mappings.items()
        self.web_server = web.Application()
        self.port = port
        self.host = host
        self.server_kwargs = server_kwargs
        self.server_args = server_args

    def transform_mappings(self):
        transformed_mappings = []

        for i in self.mappings:
            request_type = i[1].get("type", "get")

            if request_type == "get":
                transformed_mappings.append(web.get(i[0], i[1]["mapped_method"]))
            elif request_type == "post":
                transformed_mappings.append(web.post(i[0], i[1]["mapped_method"]))
            elif request_type == "put":
                transformed_mappings.append(web.put(i[0], i[1]["mapped_method"]))
            elif request_type == "patch":
                transformed_mappings.append(web.patch(i[0], i[1]["mapped_method"]))
            elif request_type == "delete":
                transformed_mappings.append(web.delete(i[0], i[1]["mapped_method"]))
        
        return transformed_mappings

    def run_server(self):
        transformed_mappings = self.transform_mappings()
        self.web_server.add_routes(transformed_mappings)
        web.run_app(
            self.web_server,
            port=self.port,
            host=self.host,
            *self.server_args,
            **self.server_kwargs,
        )


if __name__ == "__main__":
    # HeartbeatServer().execute()
    # print(detect_ip())

    async def handlePost(request):
        print(request.remote)
        return web.Response(text=json.dumps({"message": request.remote}), content_type="text/json")

    mapping = {"/": {"type": "post", "mapped_method": handlePost}}

    def test_example_v2():
        server1 = HeartbeatServerV2(mappings=mapping, port=5000)
        # server1.run_server()
        server2 = HeartbeatServerV2(mappings=mapping, port=5001)
        # server2.run_server()
        server3 = HeartbeatServerV2(mappings=mapping, port=5002)
        # server3.run_server()
        server4 = HeartbeatServerV2(mappings=mapping, port=5003)
        # server4.run_server()

        servers = [server1, server2, server3, server4]
        processes = []

        # for i in servers:
        #     processes.append(Process(target=i.run_server))

        # for i in processes:
        #     i.start()
        
        server1.run_server()

    test_example_v2()
