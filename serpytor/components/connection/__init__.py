"""The connection module contains components for monitoring the connectivity between distributed infrastructures.

## Heartbeat Monitoring

Heartbeat Monitoring is a requirement in managing distributed architectures.

SerPyTor provides for hardware & application tracking through the use of the Connections Monitor Objects.
There are two kinds of Connection Monitor Objects:

- HeartbeatClient, and
- HeartbeatServer

### HeartbeatServer

The HeartBeatServer object is an object that creates a server, emitting the status of the hardware to clients that request it.

#### Working example:

**Objective**: Run 4 server instances (simulating 4 remote resource machines) with a simple mapping to map the output of an endpoint.
The endpoint simply returns the IP of the requesting device as a JSON response.

This is probably the simplest possible application of Heartbeat.

**Implementation**:

```python
import aiohttp
from aiohttp import web
from multiprocessing import Process
import json
from serpytor.components.connection.monitor.server import HeartbeatServer
import psutil


async def handlePost(request):
    '''Contains the mapping method that will print the IP of the request origin.
    It also returns the cpu and memory usage of the system the server instance is running on.
    '''
    print(request.remote)
    return web.Response(
        text=json.dumps(
            {
                "message": request.remote,
                "cpu": psutil.cpu_percent(),
                "memory": psutil.virtual_memory(),
            }
        ),
        content_type="text/json",
    )


mapping = {"/": {"type": "post", "mapped_method": handlePost}}


def test_example_v2():
    '''Emulate the server heartbeat instances.
    '''
    server1 = HeartbeatServer(mappings=mapping, port=5000)
    # server1.start_heartbeats()  # Uncomment this line to run the server individually.
    server2 = HeartbeatServer(mappings=mapping, port=5001)
    # server2.start_heartbeats()  # Uncomment this line to run the server individually.
    server3 = HeartbeatServer(mappings=mapping, port=5002)
    # server3.start_heartbeats()  # Uncomment this line to run the server individually.
    server4 = HeartbeatServer(mappings=mapping, port=5003)
    # server4.start_heartbeats()  # Uncomment this line to run the server individually.

    servers = [server1, server2, server3, server4]
    processes = []

    for i in servers:
        processes.append(Process(target=i.start_heartbeats))

    for i in processes:
        i.start()


test_example_v2()
```

### HeartbeatClient

The other half of the Heartbeat Monitoring facility, we have the HeartbeatClient Object.
It requests the resource pool for the availability of a resource, from the client side.

#### Working example:

**Objective**: Request the Heartbeat Server and get response regarding the resources avaiability in the servers.

```python
from serpytor.components.connection.monitor.client import HeartbeatClient

class WrappedHeartbeatClient(HeartbeatClient):
    '''Emulate the connections to the different servers from the clients.
    The server can be an instance in a remote machine, or a local instance.
    '''
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

from serpytor.components.connection.extensions.reports.crash_reports.crash_reports import (
    get_report,
)
from serpytor.components.connection.monitor.monitor import Monitor
from serpytor.components.connection.monitor.client import HeartbeatClient
from serpytor.components.connection.monitor.server import HeartbeatServer
from serpytor.components.connection.monitor.gateway import Gateway

__all__ = [
    "get_report",
    "Monitor",
    "HeartbeatClient",
    "HeartbeatServer",
    "Gateway",
]
