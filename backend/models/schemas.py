from pydantic import BaseModel, Field
from typing import List, Optional

class TripIntentRequest(BaseModel):
    query: str = Field(..., example="Plan a 3-day trip to Tokyo focused on sushi and tech.")

class CityMarker(BaseModel):
    name: str
    lat: float
    lng: float
    description: Optional[str] = None
    type: str = "attraction" # e.g., restaurant, museum, park

class TripIntentResponse(BaseModel):
    intent: str
    cities: List[str]
    markers: List[CityMarker]

class ItineraryRequest(BaseModel):
    points: List[str] # List of place IDs or names

class ItineraryStep(BaseModel):
    instruction: str
    distance: str
    duration: str

class ItineraryResponse(BaseModel):
    steps: List[ItineraryStep]
    total_distance: str
    total_duration: str
    map_polyline: str
