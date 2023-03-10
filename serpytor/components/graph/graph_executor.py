import asyncio
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple

import matplotlib.pyplot as plt
import networkx as nx
import pyvis

from serpytor.components.connection import Gateway
from serpytor.components.graph.graph import Graph
from serpytor.components.graph.node import Node


class GraphExecutor:
    """## GraphExecutor Class

    :param execution_sequence: Edges of a directed acyclic bipartite graph. Represents the execution sequence of computations
    :param gateway: The Gateway Object to use for computation.
    :param graph: The Graph to execute computations of.
    """

    def __init__(
        self,
        graph: Graph,
        gateway: Gateway,
        execution_sequence: List[Tuple[int, int]],
        **kwargs: Dict[str, Any],
    ):
        self._graph: Graph = graph
        self._execution_sequence = (
            execution_sequence
            if (isinstance(execution_sequence, List))
            else list(zip(list(range(len(graph.nodes))), list(range(len(graph.nodes)))))
        )

        self._segments: Dict[str, List[Any]] = []
        self._gateway: Gateway = gateway
        self._network_graph: Optional[nx.Graph] = None
        self._node_execution_index: Dict[Node, int] = {}

    def map_node_to_execution_index(self, node: Node) -> int:
        try:
            if self._node_execution_index == {}:
                for idx, elem in enumerate(self._graph.nodes):
                    self._node_execution_index[elem] = idx

            return self._node_execution_index[node]
        except KeyError:
            return -1

    def resolve_dependencies(
        self, execution_sequence: List[Tuple[int, int]], node: Node
    ) -> List[int]:
        """Resolve dependencies to execute the task in a given node."""

        print("Resolving dependencies for nodes...")
        self._execution_sequence = sorted(
            execution_sequence, key=lambda x: x[0]
        )  # Resolve Dependencies for nodes

        node_idx: int = self.map_node_to_execution_index(node)

        print("Node dependencies:")
        print("Node\tDepends_on")
        for idx in self._execution_sequence:
            print(f"{idx[1]}\t{idx[0]}")

        dependency_sequence = [
            x[0] for x in self._execution_sequence
        ]  # TODO: Parse Dependencies properly instead of copy pasting entire execution sequence as dependency sequence
        self._segments[node_idx] = dependency_sequence
        return dependency_sequence

    def find_node_corresponding_to_task(
        self, task: Callable[..., Any]
    ) -> Tuple[bool, Optional[Node]]:
        return next(
            (
                (True, node)
                for node in self._graph.nodes
                if task.__code__.co_cellvars == node.task.__code__.co_cellvars
            ),
            (False, None),
        )

    def execute(self, node: Node) -> None:
        """Takes in a Node as an input and executes the node in a server determined by the gateway"""
        node_found, node = self.find_node_corresponding_to_task(node())
        if not node_found:
            raise Exception("Cannot find provided task in plan!")

        dependencies: List[int] = self.resolve_dependencies(
            self._execution_sequence, node
        )

        last_output = {}
        for idx in dependencies:
            node = self._graph.nodes[idx[0]]
            self._gateway.set_task(node.execute_task)
            print(last_output)
            last_output = asyncio.run(
                # TODO: Work on Node Task execution with args and kwargs
                self._gateway.execute(node.task)  # , task_kwargs=last_output)
            )
            # last_output = {"num": last_output}
        print(last_output)

    @property
    def execution_sequence(self) -> List[Tuple[int, int]]:
        return self._execution_sequence

    def set_execution_sequence(self, execution_sequence: List[Tuple[int, int]]) -> None:
        """Set the execution sequence manually.
        **Warning**: This will override any checks for dependency integrity!
        """
        self._execution_sequence = execution_sequence

    def generate_graph(
        self,
        file_loc: Optional[str] = None,
        use: Literal["pyvis", "networkx"] = "networkx",
        **kwargs,
    ) -> str:
        """Generate a visual graph using a particular backend.
        :params use: The backend to use, either "pyvis"(PyVis), or "networkx" (NetworkX raw). Defaults to "networkx".
        :params file_loc: The file location to save the output to. For use="networkx", it should be an image, and for "pyvis", an html file.
        """
        if use == "networkx":
            G = nx.DiGraph()
        elif use == "pyvis":
            G = pyvis.network.Network(directed=True)

        nodes_to_add: List[Node] = []

        for i in self._execution_sequence:
            nodes_to_add.extend((self._graph.nodes[i[0]], self._graph.nodes[i[1]]))
        nodes_to_add = list(set(nodes_to_add))

        for node in nodes_to_add:
            if use in ["networkx", "pyvis"]:
                G.add_node(str(node.task_meta["name"]), label=node.task_meta["name"])
        for x in self._execution_sequence:
            G.add_edge(
                str(self._graph.nodes[x[0]].task_meta["name"]),
                str(self._graph.nodes[x[1]].task_meta["name"]),
            )

        # nt = Network(directed=directed)
        # nt.from_nx(G)

        if use == "networkx":
            plt.clf()
            nx.draw(G, with_labels=True)
            plt.savefig(file_loc)
            self._network_graph = G
            # return open(file_loc, "rb").read()
        elif use == "pyvis":
            if "buttons" in kwargs:
                G.show_buttons(kwargs["buttons"])

            G.toggle_physics(status=False)
            # F.toggle_hide_edges_on_drag(status=True)
            # F.toggle_hide_nodes_on_drag(status=True)
            # graph = G.html  # .replace("body>", "div>").replace("html>", "div>")

            print("\nMaking PyVis Network...\n")
            G.generate_html(file_loc)
            self._network_graph = G
            # return open(file_loc, "r").read()
