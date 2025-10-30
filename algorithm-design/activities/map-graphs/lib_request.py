import googlemaps
from typing import Dict, List, Tuple

class GoogleMapsClient:
    def __init__(self, api_key: str):
        self._client = googlemaps.Client(key=api_key)

    def get_distance_between_points(self, origin: str, destination: str) -> Dict:
        try:
            # First get the route directions to get waypoints
            directions = self._client.directions(
                origin,
                destination,
                mode="driving",
                language="es",
                alternatives=True  # Get alternative routes if available
            )

            if not directions:
                raise Exception(f"No se pudo encontrar la ruta entre {origin} y {destination}")

            # Get the best route (first result)
            route = directions[0]
            
            # Extract waypoints (major cities/towns along the route)
            waypoints = []
            total_distance = 0
            
            for leg in route["legs"]:
                total_distance += leg["distance"]["value"]
                
                # Add significant waypoints from the route
                for step in leg["steps"]:
                    if "html_instructions" in step and any(word in step["html_instructions"].lower() 
                        for word in ["hacia", "through", "enter", "entering"]):
                        location = step.get("end_location", {})
                        waypoint_info = self._client.reverse_geocode(
                            (location.get("lat"), location.get("lng"))
                        )
                        if waypoint_info:
                            for component in waypoint_info[0]["address_components"]:
                                if "locality" in component["types"]:
                                    waypoints.append(component["long_name"])
                                    break

            return {
                "distance": total_distance / 1000,  # Convert to km
                "duration": route["legs"][0]["duration"]["text"],
                "waypoints": list(dict.fromkeys(waypoints))  # Remove duplicates while preserving order
            }
        except Exception as e:
            raise Exception(f"Error al obtener la ruta: {str(e)}")

    def get_route_info(self, waypoints: List[str]) -> List[Dict]:
        def get_route_segments(points: List[str], start_idx: int = 0) -> List[Dict]:
            if start_idx >= len(points) - 1:
                return []
            
            current_point = points[start_idx]
            next_point = points[start_idx + 1]
            
            segment_info = self.get_distance_between_points(current_point, next_point)
            segment = {
                "origin": current_point,
                "destination": next_point,
                "distance": segment_info["distance"],
                "duration": segment_info["duration"]
            }
            
            return [segment] + get_route_segments(points, start_idx + 1)
        
        return get_route_segments(waypoints)
