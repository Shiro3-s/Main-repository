from typing import Dict, List, Set, Optional

class Node:
    def __init__(self, value: str):
        self.value = value
        self.connections: List[Node] = []
    
    def add_connection(self, node: 'Node') -> None:
        if node not in self.connections:
            self.connections.append(node)
    
    def __str__(self) -> str:
        return self.value

class Graph:
    def __init__(self):
        self.nodes: Dict[str, Node] = {}
    
    def add_node(self, value: str) -> Node:
        if value not in self.nodes:
            self.nodes[value] = Node(value)
        return self.nodes[value]
    
    def add_edge(self, origin: str, destination: str) -> None:
        origin_node = self.add_node(origin)
        dest_node = self.add_node(destination)
        origin_node.add_connection(dest_node)
    
    def build_from_dict(self, adj_list: Dict[str, List[str]]) -> None:
        for origin, destinations in adj_list.items():
            for destination in destinations:
                self.add_edge(origin, destination)
    
    def get_all_nodes(self) -> Set[str]:
        all_nodes = set(self.nodes.keys())
        for node in self.nodes.values():
            for conn in node.connections:
                all_nodes.add(conn.value)
        return all_nodes
    
    def print_graph(self) -> None:
        for node_value, node in self.nodes.items():
            connections = [str(conn) for conn in node.connections]
            if connections:
                print(f"{node_value.capitalize()} -> {', '.join(conn.capitalize() for conn in connections)}")

def binary_search(sorted_list: List[str], target: str, left: int, right: int):
    if right is None:
        right = len(sorted_list) - 1
    if left > right:
        return False
    
    middle = (left + right) // 2
    middle_value = sorted_list[middle]

    if middle_value == target:
        return True
    elif middle_value < target:
        return binary_search(sorted_list, target, middle + 1, right)
    else:
        return binary_search(sorted_list, target, left, middle - 1)