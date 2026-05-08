import os
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from models.schemas import TripIntentRequest, TripIntentResponse, ItineraryRequest, ItineraryResponse
from services.gemini_service import GeminiService
from services.maps_service import MapsService
from services.secret_service import SecretService
from services.logging_service import LoggingService
from middleware.iap_auth import IAPAuthMiddleware

app = FastAPI(title="Orbit Travel Engine")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Project Configuration
PROJECT_ID = "travelplanner-495705"
ENV = os.getenv("ENV", "dev")

# Initialize Services
secret_service = SecretService(PROJECT_ID)
logger = LoggingService(PROJECT_ID)

# Global service instances (initialized on first request if keys available)
gemini_service = None
maps_service = None

def get_services():
    global gemini_service, maps_service
    if not gemini_service or not maps_service:
        MAPS_API_KEY = secret_service.get_secret("MAPS_API_KEY")
        GEMINI_API_KEY = secret_service.get_secret("GEMINI_API_KEY")
        
        if MAPS_API_KEY and not maps_service:
            maps_service = MapsService(MAPS_API_KEY)
        if GEMINI_API_KEY and not gemini_service:
            gemini_service = GeminiService(GEMINI_API_KEY)
    
    return gemini_service, maps_service

# Routes
@app.post("/api/intent", response_model=TripIntentResponse)
async def extract_intent(request: TripIntentRequest):
    logger.info(f"Processing trip intent for: {request.query}")
    g_service, _ = get_services()
    if not g_service:
        raise HTTPException(status_code=503, detail="Gemini service not initialized. Check API keys.")
    try:
        result = await g_service.parse_trip_intent(request.query)
        return result
    except Exception as e:
        logger.error(f"Error in extract_intent: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/itinerary", response_model=ItineraryResponse)
async def generate_itinerary(request: ItineraryRequest):
    logger.info(f"Generating itinerary for {len(request.points)} points")
    _, m_service = get_services()
    if not m_service:
        raise HTTPException(status_code=503, detail="Maps service not initialized. Check API keys.")
    try:
        result = m_service.get_optimized_itinerary(request.points)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        # Record custom metric
        logger.record_itinerary_generation()
        return result
    except Exception as e:
        logger.error(f"Error in generate_itinerary: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
