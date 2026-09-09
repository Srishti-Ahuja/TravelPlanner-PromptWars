import requests
from typing import Dict, List
import json
import logging
import time
from ..models.schemas import ChatMessage, Waypoint

logger = logging.getLogger(__name__)

class GeminiService:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={self.api_key}"
        logger.info("GeminiService initialized with gemini-2.5-flash via REST API")

    async def parse_trip_intent(self, query: str) -> Dict:
        prompt = f"""
        Extract trip intent and specific places of interest from the following query: "{query}"
        Return ONLY a valid JSON object with this exact structure:
        {{
            "intent": "Short summary of the user's travel goal",
            "cities": ["List of city names mentioned or implied"],
            "markers": [
                {{
                    "name": "Name of specific place",
                    "lat": 0.0,
                    "lng": 0.0,
                    "description": "Brief reason for including this place",
                    "type": "attraction",
                    "rating": 4.5,
                    "image_keyword": "single_keyword_for_image_search"
                }}
            ]
        }}
        Provide a realistic float rating out of 5.0 for the place. Provide a single descriptive keyword (no spaces, e.g. "tokyotower") for image_keyword.
        Use accurate real-world coordinates. Return 5-8 diverse markers (attractions, restaurants, hotels, transit).
        Return ONLY the JSON, no markdown code blocks.
        """
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }],
            "generationConfig": {
                "temperature": 0.1
            }
        }
        
        try:
            response = requests.post(self.url, json=payload, headers={'Content-Type': 'application/json'})
            response.raise_for_status()
            data = response.json()
            
            text = data['candidates'][0]['content']['parts'][0]['text'].strip()
            
            if text.startswith("```"):
                text = text.split("```")[1]
                if text.startswith("json"):
                    text = text[4:]
            return json.loads(text.strip())
        except Exception as e:
            logger.error(f"Error parsing Gemini response: {e}")
            return {
                "intent": f"Travel to {query}",
                "cities": [query],
                "markers": []
            }

    async def chat_itinerary(self, points: List[Waypoint], chat_history: List[ChatMessage], user_message: str) -> str:
        # If fewer than 2 points, we might want to clear context or handle differently
        if len(points) < 2:
            places_str = "No specific locations selected yet."
        else:
            places_str = ", ".join([p.name for p in points])
            
        system_prompt = f"""
        You are the Orbit Travel Agent. The user is planning an itinerary and has explicitly selected these places: {places_str}.
        Make sure the itinerary focuses specifically on these places, though you may suggest a few related additions.
        Keep responses helpful, engaging, and format them nicely in HTML (use <b>, <ul>, <li>, <br>). Do not use markdown.
        """
        contents = [{"role": "user", "parts": [{"text": system_prompt}]}]
        contents.append({"role": "model", "parts": [{"text": "Understood. How can I help with this itinerary?"}]})
        for msg in chat_history:
            contents.append({"role": msg.role, "parts": [{"text": msg.content}]})
        contents.append({"role": "user", "parts": [{"text": user_message}]})
        payload = {
            "contents": contents,
            "generationConfig": {"temperature": 0.7}
        }
        # Retry up to 3 times on rate limit (429) errors
        retries = 3
        backoff = 2  # seconds
        for attempt in range(retries):
            try:
                response = requests.post(self.url, json=payload, headers={'Content-Type': 'application/json'})
                response.raise_for_status()
                data = response.json()
                return data['candidates'][0]['content']['parts'][0]['text'].strip()
            except requests.HTTPError as e:
                if response.status_code == 429:
                    logger.warning(f"Gemini rate limit hit, attempt {attempt + 1}/{retries}. Retrying in {backoff}s.")
                    time.sleep(backoff)
                    backoff *= 2
                    continue
                else:
                    logger.error(f"Error in chat_itinerary: {e}")
                    break
            except Exception as e:
                logger.error(f"Unexpected error in chat_itinerary: {e}")
                break
        return "I'm sorry, I'm having trouble generating a response right now."
