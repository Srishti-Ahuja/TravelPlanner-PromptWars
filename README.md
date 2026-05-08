# Orbit: Travel Planning & Experience Engine 🌍

Orbit is a premium, AI-powered travel planning application that leverages Gemini 1.5 Flash and Google Maps Grounding to transform natural language intent into actionable itineraries.

## 🏛 System Architecture

- **Frontend**: React (Vite) + Tailwind CSS.
  - Implements "Modern Nomad" aesthetic with glassmorphism.
  - Debounced chat interface (500ms) for real-time map updates.
  - Google One Tap Login for seamless authentication.
- **Backend**: FastAPI (Python).
  - **Gemini Service**: Extracts trip intent and markers using Google Maps Grounding.
  - **Maps Service**: Calculates optimized routes using Google Maps Routes API.
  - **Observability**: Integrates Google Cloud Logging & Monitoring (custom metrics).
- **Security**: 
  - Protected by Identity-Aware Proxy (IAP) on Cloud Run.
  - Secrets managed via GCP Secret Manager.

## 🚀 Setup Instructions

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repo-url>
   cd TravelPlanner-PromptWars
   ```

2. **Backend Setup**:
   ```bash
   cd backend
   pip install -r requirements.txt
   export GOOGLE_CLOUD_PROJECT="travelplanner-495705"
   # For local dev, you can use .env for API keys
   uvicorn main:app --reload
   ```

3. **Frontend Setup**:
   ```bash
   cd frontend
   npm install
   # Create .env: VITE_MAPS_API_KEY=your_key
   npm run dev
   ```

### GCP Deployment

1. **Authenticate**:
   ```cmd
   gcloud auth login
   gcloud config set project travelplanner-495705
   ```

2. **Build and Deploy to Cloud Run**:
   ```bash
   gcloud builds submit --tag gcr.io/travelplanner-495705/orbit-backend
   gcloud run deploy orbit-backend --image gcr.io/travelplanner-495705/orbit-backend --platform managed
   ```

3. **Enable IAP**:
   - Go to GCP Console -> Security -> IAP.
   - Enable IAP for the Cloud Run service.

## 🔑 Environment Variables

| Variable | Description | Source |
|----------|-------------|--------|
| `MAPS_API_KEY` | Google Maps API Key | Secret Manager |
| `GEMINI_API_KEY` | Google AI Studio Key | Secret Manager |
| `PROJECT_ID` | GCP Project ID | Hardcoded/Env |

## 💰 Cost Optimization ($5/mo Strategy)

Orbit is designed to stay within the free tier or a minimal $5 budget:
- **Debouncing**: Chat input is debounced by 500ms to prevent excessive Gemini/Maps API calls while typing.
- **Gemini 1.5 Flash**: Uses the most cost-efficient model for extraction.
- **Caching**: API keys and frequently accessed metadata are cached in memory.
- **Quota Management**: Custom Cloud Monitoring alerts are set to notify at 80% of the $5 budget.
- **Serverless**: Cloud Run scales to zero when not in use, incurring zero cost for idle time.

## ♿ Accessibility (WCAG 2.1)
- Focus rings for keyboard navigation.
- Skip links for "Skip to Map" and "Skip to List".
- ARIA roles and labels for dynamic components.
- Contrast ratios exceeding 4.5:1.
