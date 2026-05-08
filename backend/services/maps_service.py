import googlemaps
from datetime import datetime
from typing import List, Dict

class MapsService:
    def __init__(self, api_key: str):
        self.gmaps = googlemaps.Client(key=api_key)

    def get_optimized_itinerary(self, points: List[str]) -> Dict:
        """
        Calculates an optimized route between multiple points using the Directions API.
        """
        if len(points) < 2:
            return {"error": "At least two points required for a route."}

        # Request directions with waypoint optimization
        now = datetime.now()
        directions_result = self.gmaps.directions(
            origin=points[0],
            destination=points[-1],
            waypoints=points[1:-1],
            optimize_waypoints=True,
            departure_time=now
        )

        if not directions_result:
            return {"error": "No route found."}

        route = directions_result[0]
        legs = route['legs']
        
        steps = []
        total_distance = 0
        total_duration = 0
        
        for leg in legs:
            total_distance += leg['distance']['value']
            total_duration += leg['duration']['value']
            for step in leg['steps']:
                steps.append({
                    "instruction": step['html_instructions'],
                    "distance": step['distance']['text'],
                    "duration": step['duration']['text']
                })

        return {
            "steps": steps,
            "total_distance": f"{total_distance / 1000:.1f} km",
            "total_duration": f"{total_duration // 3600}h { (total_duration % 3600) // 60}m",
            "map_polyline": route['overview_polyline']['points']
        }
