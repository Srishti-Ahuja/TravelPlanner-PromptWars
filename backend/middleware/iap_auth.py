from fastapi import Request, HTTPException, status
from jose import jwt
import requests
import time

# IAP Public Key discovery URL
KEYS_URL = "https://www.gstatic.com/iap/verify/public_key"

class IAPAuthMiddleware:
    def __init__(self, project_number: str, backend_service_id: str):
        self.expected_audience = f"/projects/{project_number}/global/backendServices/{backend_service_id}"
        self.keys = {}
        self.last_key_refresh = 0

    def refresh_keys(self):
        if time.time() - self.last_key_refresh > 3600: # Refresh every hour
            resp = requests.get(KEYS_URL)
            self.keys = resp.json()
            self.last_key_refresh = time.time()

    async def __call__(self, request: Request, call_next):
        # Skip auth for local development if needed, or check header
        iap_jwt = request.headers.get("X-Goog-IAP-JWT-Assertion")
        
        # If no header, and we are in production, fail
        if not iap_jwt:
            # Allow skipping for local dev if environment variable is set
            import os
            if os.getenv("ENV") == "dev":
                return await call_next(request)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing IAP JWT header"
            )

        try:
            self.refresh_keys()
            # Decode and verify the token
            decoded_jwt = jwt.decode(
                iap_jwt,
                self.keys,
                algorithms=["ES256"],
                audience=self.expected_audience
            )
            # Store user info in request state
            request.state.user = decoded_jwt
            return await call_next(request)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"Invalid IAP JWT: {str(e)}"
            )
