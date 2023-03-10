from functools import wraps, partial
from typing import List, Dict, Any, Callable, Union, Optional
from serpytor.components.graph import Node


class Graph:
    def __init__(
        self,
        description: Optional[str] = "",
        title: Optional[str] = "SerPyTor Graph v0.1",
        directed: bool = False,
        **kwargs
    ):
        self._meta: Dict[str, Any] = {"description": description, "title": title}

        self._directed: bool = directed
        self._nodes: List[Node] = kwargs.get("nodes", [])
        self._edges: List[Any] = kwargs.get("edges", [])

    @property
    def nodes(self):
        return self._nodes

    def add_node(self, node: Node):
        self.nodes.append(node)

    def show_nodes(self):
        for node in self.nodes:
            print(node.task_meta)

    def add_edge(self, edge: Any):
        self.edges.append(edge)

    def add_to_graph(
        self,
        task: Callable[..., Any],
        node_params: Optional[Dict[str, Any]] = {},
        graph_addition_params: Optional[Dict[str, Any]] = {},
    ) -> Callable[..., Any]:
        @wraps(task)
        def wrapper(**kwargs):
            self.add_node(
                Node(task, task_params=node_params | kwargs), **graph_addition_params
            )
            return task

        return wrapper


if __name__ == "__main__":
    graph: Graph = Graph()

    @graph.add_to_graph
    def hello():
        print("Hi!")

    def main():
        hello()
        print(graph.nodes)
        print("Nodes with metadata - ")
        print(graph.show_nodes())

    main()
