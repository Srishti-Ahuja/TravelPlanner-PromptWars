import google.generativeai as genai
from typing import List, Dict
import json
from models.schemas import CityMarker

class GeminiService:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        # Using Gemini 2.5 as requested
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    async def parse_trip_intent(self, query: str) -> Dict:
        prompt = f"""
        Extract trip intent and specific places of interest from the following query: "{query}"
        Return a JSON object with the following structure:
        {{
            "intent": "Short summary of the user's travel goal",
            "cities": ["List of city names mentioned or implied"],
            "markers": [
                {{
                    "name": "Name of specific place",
                    "lat": 0.0,
                    "lng": 0.0,
                    "description": "Brief reason for including this place",
                    "type": "attraction|restaurant|hotel|transit"
                }}
            ]
        }}
        Use Google Maps data to provide accurate coordinates for the markers. 
        Focus on providing a variety of high-quality markers.
        """
        
        response = self.model.generate_content(prompt)
        try:
            # Clean response text if needed (sometimes gemini wraps in ```json)
            text = response.text
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            return json.loads(text)
        except Exception as e:
            print(f"Error parsing Gemini response: {e}")
            return {
                "intent": "Error parsing intent",
                "cities": [],
                "markers": []
            }
