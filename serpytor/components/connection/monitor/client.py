import requests
import time


class HeartbeatClient:
    def __init__(
        self,
        default_endpoint: str = "http://172.16.25.252:6666",
        time_interval: float = 2.5,
        *args: list,
        **kwargs: dict,
    ):
        self.type = "Client"
        self.time_interval: float = time_interval
        self.default_endpoint: str = default_endpoint

    def send_request(self, endpoint: str = "") -> None:
        if not endpoint:
            endpoint = self.default_endpoint
        print("Sending GET request to:", endpoint)
        requests.get(endpoint)

    def start_heartbeat(self) -> None:
        try:
            while True:
                self.send_request()
                time.sleep(self.time_interval)
        except KeyboardInterrupt:
            print("Shutting down client...")
        except Exception as e:
            print(f"Exception details: {e}")


if __name__ == "__main__":
    client = HeartbeatClient()
    client.start_heartbeat()
