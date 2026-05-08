import requests

def check_iap_protection(url):
    """
    Check if a URL is protected by IAP.
    Expects a 401 or 302 redirect to Google Login if not authenticated.
    """
    print(f"Checking IAP protection for: {url}")
    try:
        response = requests.get(url, allow_redirects=False)
        
        if response.status_code in [302, 401]:
            print("✅ SUCCESS: Request was blocked/redirected (IAP likely active).")
        else:
            print(f"❌ WARNING: Request returned {response.status_code}. IAP might NOT be active or misconfigured.")
            
    except Exception as e:
        print(f"Error checking IAP: {e}")

if __name__ == "__main__":
    # Example usage for deployed service
    # check_iap_protection("https://orbit-backend-travelplanner-495705.a.run.app/health")
    
    print("--- IAP Security Checklist ---")
    print("1. [ ] Cloud Run service 'Authentication' set to 'Require IAM authentication'.")
    print("2. [ ] IAP enabled for the backend service in Google Cloud Console.")
    print("3. [ ] Middleware in backend/middleware/iap_auth.py active and checking 'X-Goog-IAP-JWT-Assertion'.")
    print("4. [ ] Service account for Cloud Run has 'IAP-secured Web App User' role if needed.")
    print("5. [ ] Audience (AUD) in JWT validation matches the IAP resource ID.")
