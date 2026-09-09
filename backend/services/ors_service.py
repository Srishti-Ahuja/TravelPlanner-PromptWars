import openrouteservice
from openrouteservice.geocode import pelias_search
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

class ORSService:
    def __init__(self, api_key: str):
        self.client = openrouteservice.Client(key=api_key)
        logger.info("ORSService initialized")

    def geocode_place(self, place_name: str) -> List[float]:
        """Returns [lng, lat] for a place name."""
        try:
            result = self.client.pelias_search(text=place_name, size=1)
            coords = result['features'][0]['geometry']['coordinates']  # [lng, lat]
            return coords
        except Exception as e:
            logger.error(f"Geocoding failed for '{place_name}': {e}")
            raise ValueError(f"Could not geocode '{place_name}'")

    def get_optimized_itinerary(self, points: List) -> Dict:
        """
        Takes coordinates directly and returns optimized route.
        Returns steps, total_distance, total_duration, and decoded polyline coords.
        """
        if len(points) < 2:
            return {"error": "At least two points required."}

        # Use coords directly from Waypoints
        coords = [[p.lng, p.lat] for p in points]

        try:
            # ORS directions
            routes = self.client.directions(
                coordinates=coords,
                profile='driving-car',
                format='geojson',
                optimize_waypoints=True
            )
        except Exception as e:
            logger.error(f"ORS directions error: {e}")
            return {"error": f"Routing error: {e}"}

        feature = routes['features'][0]
        props = feature['properties']
        summary = props['summary']
        segments = props['segments']

        # Build steps list from all segments
        steps = []
        for segment in segments:
            for step in segment['steps']:
                steps.append({
                    "instruction": step.get('instruction', ''),
                    "distance": f"{step['distance'] / 1000:.1f} km" if step['distance'] >= 1000 else f"{step['distance']:.0f} m",
                    "duration": f"{int(step['duration'] // 60)} min"
                })

        # Total stats
        total_dist_km = summary['distance'] / 1000
        total_dur_min = int(summary['duration'] // 60)
        hours = total_dur_min // 60
        mins = total_dur_min % 60

        # Polyline from GeoJSON geometry — list of [lng, lat]
        geom_coords = feature['geometry']['coordinates']  # [[lng, lat], ...]
        # Convert to {lat, lng} dicts for Leaflet
        polyline_points = [{"lat": c[1], "lng": c[0]} for c in geom_coords]

        return {
            "steps": steps,
            "total_distance": f"{total_dist_km:.1f} km",
            "total_duration": f"{hours}h {mins}m",
            "map_polyline": polyline_points
        }
