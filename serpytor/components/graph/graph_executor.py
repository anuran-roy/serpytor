from typing import Dict, Any, List, Literal, Optional, Tuple
from serpytor.components.graph.graph import Graph
from serpytor.components.connection import Gateway
import asyncio
import networkx as nx
import pyvis
import matplotlib.pyplot as plt

from serpytor.components.graph.node import Node


class GraphExecutor:
    """## GraphExecutor Class

    :param execution_sequence: Edges of a directed acyclic bipartite graph. Represent the execution sequence of computations
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
            if (type(execution_sequence) == type([]))
            else list(zip(list(range(len(graph.nodes))), list(range(len(graph.nodes)))))
        )

        self._gateway: Gateway = gateway
        self.network_graph: Optional[nx.Graph] = None

    def resolve_dependencies(
        self, execution_sequence: List[Tuple[int, int]], node: Node
    ) -> List[int]:
        """Resolve dependencies to execute the task in a given node."""

        print("Resolving dependencies for nodes...")
        self._execution_sequence = sorted(
            execution_sequence, key=lambda x: x[0]
        )  # Resolve Dependencies for nodes

        print("Node dependencies:")
        print("Node\tDepends_on")
        for idx in self._execution_sequence:
            print(f"{idx[1]}\t{idx[0]}")

    def execute(self, node: Node) -> None:
        dependencies: List[int] = self.resolve_dependencies(
            self._execution_sequence, node
        )

        last_output = {}
        for idx in dependencies:
            node = self._graph.nodes[idx[0]]
            self._gateway.set_task(node.execute_task)
            print(last_output)
            last_output = asyncio.run(
                self._gateway.execute(node.task, task_kwargs=last_output)
            )
            last_output = {"num": last_output}
        print(last_output)

    def set_execution_sequence(self, execution_sequence: List[Tuple[int, int]]) -> None:
        self._execution_sequence = execution_sequence

    def generate_graph(
        self,
        file_loc: Optional[str] = None,
        directed: bool = True,
        use: Literal["pyvis", "networkx"] = "networkx",
        **kwargs,
    ) -> str:
        """ """
        if use == "networkx":
            G = nx.DiGraph()
        elif use == "pyvis":
            G = pyvis.network.Network(directed=True)

        nodes_to_add: List[Node] = []

        for i in self._execution_sequence:
            nodes_to_add.append(self._graph.nodes[i[0]])
            nodes_to_add.append(self._graph.nodes[i[1]])

        nodes_to_add = list(set(nodes_to_add))

        for idx, node in enumerate(nodes_to_add):
            if use == "networkx":
                G.add_node(str(node.task_meta["name"]), label=node.task_meta["name"])
            elif use == "pyvis":
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
            self.network_graph = G
            return open(file_loc, "rb").read()
        elif use == "pyvis":
            if "buttons" in kwargs.keys():
                G.show_buttons(kwargs["buttons"])

            G.toggle_physics(status=False)
            # F.toggle_hide_edges_on_drag(status=True)
            # F.toggle_hide_nodes_on_drag(status=True)
            # graph = G.html  # .replace("body>", "div>").replace("html>", "div>")

            print("\nMaking PyVis Network...\n")
            G.generate_html(file_loc)
            self.network_graph = G
            return open(file_loc, "r").read()


if __name__ == "__main__":
    from serpytor.components.connection.monitor.gateway import Gateway

    graph_executor = GraphExecutor()
    graph_executor.execute()
