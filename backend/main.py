import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
load_dotenv()

from .models.schemas import TripIntentRequest, TripIntentResponse, ItineraryRequest, ItineraryResponse, ItineraryChatRequest, ItineraryChatResponse
from .services.gemini_service import GeminiService
try:
    from .services.ors_service import ORSService
except Exception:
    ORSService = None  # Fallback if ORSService not available

# Configure stdlib logging (visible in Render dashboard)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("orbit_app")

app = FastAPI(title="Orbit Travel Engine")

# CORS — allow all origins (lock down to frontend URL in production if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Read secrets from environment variables (set in Render dashboard)
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
ORS_API_KEY = os.environ.get("ORS_API_KEY", "")

# Lazy-initialized service instances
_gemini_service = None
_ors_service = None

class MockGeminiService:
    async def chat_itinerary(self, points, chat_history, user_message):
        # Simple mock response for testing without real Gemini API
        return f"Mock response for message: {user_message}" 
    async def parse_trip_intent(self, query):
        return {"intent": "mock", "cities": [], "markers": []}

class MockORSService:
    def get_optimized_itinerary(self, points):
        if len(points) < 2:
            return {"error": "At least two points required."}
        polyline = [{"lat": p.lat, "lng": p.lng} for p in points]
        steps = [{"instruction": f"Visit {getattr(p, 'name', 'point')}", "distance": "0 km", "duration": "0 min"} for p in points]
        return {"steps": steps, "total_distance": "0 km", "total_duration": "0 min", "map_polyline": polyline}

# Modify get_gemini to use mock when key not set
def get_gemini():
    global _gemini_service
    if _gemini_service is None:
        # Use real Gemini if API key is provided, otherwise fall back to mock
        api_key = os.getenv('GEMINI_API_KEY')
        if api_key:
            logger.info('Initializing real GeminiService')
            _gemini_service = GeminiService(api_key)
        else:
            logger.info('Using MockGeminiService for Gemini interactions')
            _gemini_service = MockGeminiService()
    return _gemini_service

def get_ors():
    global _ors_service
    if _ors_service is None:
        api_key = os.getenv('ORS_API_KEY')
        if api_key and ORSService:
            logger.info('Initializing real ORSService')
            _ors_service = ORSService(api_key)
        else:
            logger.info('Using MockORSService for ORS interactions')
            _ors_service = MockORSService()
    return _ors_service

# ── Routes ──────────────────────────────────────────────────────────────────




@app.post("/api/intent", response_model=TripIntentResponse)
async def extract_intent(request: TripIntentRequest):
    logger.info(f"Intent request: {request.query}")
    try:
        result = await get_gemini().parse_trip_intent(request.query)
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in extract_intent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/itinerary", response_model=ItineraryResponse)
async def generate_itinerary(request: ItineraryRequest):
    logger.info(f"Itinerary request for {len(request.points)} points: {request.points}")
    try:
        result = get_ors().get_optimized_itinerary(request.points)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in generate_itinerary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/itinerary/chat", response_model=ItineraryChatResponse)
async def chat_itinerary(request: ItineraryChatRequest):
    logger.info(f"Itinerary chat request for {len(request.points)} points with message: {request.user_message}")
    try:
        response_text = await get_gemini().chat_itinerary(request.points, request.chat_history, request.user_message)
        return ItineraryChatResponse(message=response_text)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in chat_itinerary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 10001))
    uvicorn.run(app, host="0.0.0.0", port=port)
