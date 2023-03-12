from typing import Any, Callable, Dict, List, Tuple, Union

from serpytor.components.connection.monitor.gateway import Gateway
from serpytor.components.connection.monitor.server import Server
from serpytor.components.utils.algorithms.allocation.base_allocation import \
    BaseAllocation
from serpytor.components.utils.algorithms.allocation.fcfs_allocation import \
    FCFSAllocation


class GatewayServer:
    def __init__(
        self,
        mappings: Dict[str, Dict[str, Union[str, Callable]]] = {},
        heartbeat_addresses: List[str] = [],
        resource_addresses: List[str] = [],
        gateway_allocation_mechanism: BaseAllocation = FCFSAllocation(),
        task_setup_data: Tuple[List[Any], Dict[str, Any]] = ([], {}),
        *args: List[Any],
        **kwargs: Dict[str, Any]
    ) -> None:
        self._gateway_allocation_mechanism = gateway_allocation_mechanism
        self._heartbeat_addresses = heartbeat_addresses
        self._resource_addresses = resource_addresses
        self._task_setup_data = task_setup_data
        self._server_mappings = mappings
        self._gateway = Gateway(
            task=lambda x: x,
            allocation_algorithm=FCFSAllocation,
            heartbeat_addresses=self._heartbeat_addresses,
            resource_addresses=self._resource_addresses,
            gateway_allocation_mechanism=self._gateway_allocation_mechanism,
            task_setup_data=self._task_setup_data,
        )
        self._server = Server(
            mappings=self._server_mappings,
            server_port=kwargs.get("port", 9000),
            server_host=kwargs.get("server_host", "localhost"),
        )

    def start(self) -> None:
        self._server.execute()


if __name__ == "__main__":
    gateway_server = GatewayServer()

    gateway_server.start()
