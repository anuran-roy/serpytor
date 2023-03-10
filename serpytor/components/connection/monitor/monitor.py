from yaml import safe_load

from serpytor.components.connection.monitor.server import HeartbeatServer


class Monitor:
    def __init__(self) -> None:
        self.config = safe_load(open("./monitor_config.yml", "r").read())
        self.clients = self.config["devices"]["clients"]["allow"]
        self.servers = self.config["devices"]["servers"]["allow"]

    def start_server(self) -> None:
        server = HeartbeatServer()
        server.start_heartbeats()
