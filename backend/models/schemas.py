from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class TripIntentRequest(BaseModel):
    query: str = Field(..., example="Plan a 3-day trip to Tokyo focused on sushi and tech.")

class CityMarker(BaseModel):
    name: str
    lat: float
    lng: float
    description: Optional[str] = None
    type: str = "attraction"
    rating: Optional[float] = None
    image_keyword: Optional[str] = None

class TripIntentResponse(BaseModel):
    intent: str
    cities: List[str]
    markers: List[CityMarker]

class Waypoint(BaseModel):
    name: str
    lat: float
    lng: float

class ItineraryRequest(BaseModel):
    points: List[Waypoint]

class ItineraryStep(BaseModel):
    instruction: str
    distance: str
    duration: str

class ItineraryResponse(BaseModel):
    steps: List[ItineraryStep]
    total_distance: str
    total_duration: str
    map_polyline: List[Dict]  # List of {lat, lng} for Leaflet - changed from encoded str

class ChatMessage(BaseModel):
    role: str # "user" or "model"
    content: str

class ItineraryChatRequest(BaseModel):
    points: List[Waypoint]
    chat_history: List[ChatMessage]
    user_message: str

class ItineraryChatResponse(BaseModel):
    message: str
