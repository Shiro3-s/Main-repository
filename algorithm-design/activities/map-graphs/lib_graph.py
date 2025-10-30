from typing import Dict, List, Set, Optional
from dataclasses import dataclass

@dataclass
class Edge:
    destination: str
    distance: float
    duration: str

class Graph:
    def __init__(self):
        self._adjacency_list: Dict[str, List[Edge]] = {}

    def add_vertex(self, city: str) -> None:
        if city not in self._adjacency_list:
            self._adjacency_list[city] = []

    def add_edge(self, origin: str, destination: str, distance: float, duration: str) -> None:
        self.add_vertex(origin)
        self.add_vertex(destination)
        
        # Add edge in both directions (undirected graph)
        self._adjacency_list[origin].append(Edge(destination, distance, duration))
        self._adjacency_list[destination].append(Edge(origin, distance, duration))

    def find_optimal_route(self, origin: str, destination: str, intermediate_points: List[str] = None) -> List[Dict]:
        def find_shortest_path(current: str, target: str, visited: Set[str]) -> Optional[List[Dict]]:
            if current == target:
                return []
            
            if current not in self._adjacency_list:
                return None
            
            visited.add(current)
            shortest_path = None
            min_distance = float('inf')
            
            for edge in self._adjacency_list[current]:
                if edge.destination not in visited:
                    path = find_shortest_path(edge.destination, target, visited.copy())
                    if path is not None:
                        total_distance = edge.distance + sum(segment["distance"] for segment in path)
                        if total_distance < min_distance:
                            min_distance = total_distance
                            shortest_path = [
                                {
                                    "origin": current,
                                    "destination": edge.destination,
                                    "distance": edge.distance,
                                    "duration": edge.duration
                                }
                            ] + path
            
            return shortest_path

        if not intermediate_points:
            return find_shortest_path(origin, destination, set())
        
        # Handle route with intermediate points
        points = [origin] + intermediate_points + [destination]
        complete_route = []
        
        for i in range(len(points) - 1):
            segment = find_shortest_path(points[i], points[i + 1], set())
            if segment is None:
                raise Exception(f"No se pudo encontrar ruta entre {points[i]} y {points[i + 1]}")
            complete_route.extend(segment)
        
        return complete_route
