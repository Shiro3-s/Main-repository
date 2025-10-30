from lib_request import GoogleMapsClient
from lib_graph import Graph
from typing import List, Dict

def create_route_graph(client: GoogleMapsClient, cities: List[str]) -> Graph:
    """
    Create a graph from a list of cities using Google Maps data
    Args:
        client (GoogleMapsClient): Google Maps API client
        cities (List[str]): List of cities to connect
    Returns:
        Graph: Graph with cities and their connections
    """
    graph = Graph()
    
    # Add edges between all cities (complete graph)
    for i in range(len(cities)):
        for j in range(i + 1, len(cities)):
            route_info = client.get_distance_between_points(cities[i], cities[j])
            graph.add_edge(
                cities[i],
                cities[j],
                route_info["distance"],
                route_info["duration"]
            )
    
    return graph

def print_route_summary(route: List[Dict]) -> None:
    """
    Print a summary of the route including distances and total distance
    Args:
        route (List[Dict]): List of route segments
    """
    total_distance = 0
    print("\nResumen de la ruta:")
    print("-" * 50)
    
    for segment in route:
        print(f"De {segment['origin']} a {segment['destination']}:")
        print(f"  Distancia: {segment['distance']:.2f} km")
        print(f"  Duración estimada: {segment['duration']}")
        print("-" * 50)
        total_distance += segment['distance']
    
    print(f"\nDistancia total del recorrido: {total_distance:.2f} km")

def main():
    # Replace with your Google Maps API key
    API_KEY = "AIzaSyBYgedUqCjlyF-Dr9-qhiv8SThIFvniLWo"
    
    # Initialize the Google Maps client
    maps_client = GoogleMapsClient(API_KEY)
    
    # Get input from user
    print("\n=== Buscador de Rutas Óptimas ===")
    origin = input("Ciudad de origen: ").strip()
    destination = input("Ciudad de destino: ").strip()
    
    try:
        # Get route information including suggested waypoints
        route_info = maps_client.get_distance_between_points(origin, destination)
        
        # If we have waypoints, use them to create a more detailed route
        waypoints = route_info.get("waypoints", [])
        
        if waypoints:
            print("\nPuntos intermedios importantes detectados:", ", ".join(waypoints))
            
            # Create a graph with origin, destination and detected waypoints
            all_cities = [origin] + waypoints + [destination]
            route_graph = create_route_graph(maps_client, all_cities)
            
            # Find the optimal route through the waypoints
            optimal_route = route_graph.find_optimal_route(origin, destination, waypoints)
        else:
            # If no waypoints, create a simple direct route
            route_graph = create_route_graph(maps_client, [origin, destination])
            optimal_route = route_graph.find_optimal_route(origin, destination)
        
        # Print the route summary
        print_route_summary(optimal_route)
        
    except Exception as e:
        print(f"\nError: {str(e)}")

if __name__ == "__main__":
    main()
