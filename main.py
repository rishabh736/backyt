import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# This variable MUST be named 'app' for Gunicorn to find it
app = FastAPI(title="Yantra Kavach API")

# Configure CORS so your React frontend can access the data
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for development; narrow this to your React URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- API ENDPOINTS ---

@app.get("/")
async def health_check():
    """Endpoint for Render to verify the service is live."""
    return {"status": "online", "message": "Yantra Kavach Backend is Running"}

@app.get("/api/machine-health")
async def get_machine_health():
    """Main endpoint for your React dashboard."""
    return {
        "machine_id": "ML-01",
        "status": "Operational",
        "vibration_score": 0.004,
        "temperature": 42.5,
        "anomalies_detected": 0,
        "last_sync": "2026-04-09T14:50:00Z"
    }

# --- SERVER BOOTSTRAP ---

if __name__ == "__main__":
    import uvicorn
    # Render assigns a port dynamically via the PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    # We use 0.0.0.0 to make the server accessible externally on Render
    uvicorn.run(app, host="0.0.0.0", port=port)
