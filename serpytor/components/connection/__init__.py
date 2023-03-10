"""The connection module contains components for monitoring the connectivity between distributed infrastructures.

## Heartbeat Monitoring

Heartbeat Monitoring is a requirement in managing distributed architectures.

SerPyTor provides for hardware & application tracking through the use of the Connections Monitor Objects.
There are two kinds of Connection Monitor Objects:

- HeartbeatClient, and
- HeartbeatServer

### HeartbeatServer

The HeartBeatServer object is an object that creates a server, emitting the status of the hardware to clients that request it.

##### Working example:

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


async def handleGet(request):
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


mapping = {"/": {"type": "post", "mapped_method": handleGet}}


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

## Serving

SerPyTor also provides building blocks for servers, which have Heartbeat Monitoring built into them.

Currently, the `Server` object can be used to quickly spawn a server instance that has heartbeat monitoring built into it.

### Server

SerPyTor provides you with a `Server` object that can be used to create a server with inbuilt heartbeat monitoring.

```python
import psutil
from aiohttp import web
import json
from serpytor.components.connection.monitor.server import Server

async def handleGet(request):
        '''Contains the mapping method that will print the IP of the request origin.
        It also returns the cpu and memory usage of the system the server instance is running on.
        '''
        print(request.remote)
        return web.Response(
            text=json.dumps(
                {
                    "message": request.remote,
                    "cpu": psutil.cpu_percent(),
                    "memory": psutil.virtual_memory()[2],
                }
            ),
            content_type="text/json",
        )

    async def hello(request):
        print("Hello!")
        return web.Response(
            text=json.dumps({"message": "Hello!", "target": request.remote}),
            content_type="text/json",
        )

    heartbeat_mapping = {"/heartbeat": {"type": "get", "mapped_method": handleGet}}
    mapping = {"/hello": {"type": "get", "mapped_method": hello}}

server = Server(
    heartbeat_mappings=heartbeat_mapping,
    heartbeat_port=5000,
    mappings=mapping,
    server_host="127.0.0.1",
    server_port=8100,
)
```

This code spawns up a Server object instance with the User Service and the HeartBeat server.

The reasoning to separate out the Service and the HeartBeat Servers is to differentiate between resource availability and service availability.
A resource might not be available, but the resource might be, signifying an application level error.

If the resource itself isn't available, then the service is unavailable too.
"""

from serpytor.components.connection.extensions.reports.crash_reports.crash_reports import \
    get_report
from serpytor.components.connection.monitor.client import HeartbeatClient
from serpytor.components.connection.monitor.gateway import Gateway
from serpytor.components.connection.monitor.monitor import Monitor
from serpytor.components.connection.monitor.server import (HeartbeatServer,
                                                           Server)

__all__ = [
    "get_report",
    "Monitor",
    "HeartbeatClient",
    "HeartbeatServer",
    "Gateway",
    "Server",
]
