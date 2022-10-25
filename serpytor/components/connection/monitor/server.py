from aiohttp import web
from yaml import safe_load
import time
import json
from datetime import datetime
from tinydb import TinyDB, Query
from .utils import detect_ip


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


if __name__ == "__main__":
    HeartbeatServer().execute()
    # print(detect_ip())
