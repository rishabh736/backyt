import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

# The variable must be named 'app'
app = FastAPI(title="Yantra Kavach API")

# Enable CORS so your React frontend can fetch this data securely
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- ENDPOINTS ---

@app.get("/")
async def root():
    """Health check endpoint to verify the server is live."""
    return {
        "status": "online", 
        "message": "Yantra Kavach API is running on Render. Visit /api/machine-health for data."
    }

@app.get("/api/machine-health")
async def get_machine_health():
    """Main endpoint serving raw JSON telemetry data."""
    # Generate the exact current time in UTC
    current_time = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    
    return {
        "machine_id": "Yantra-01",
        "status": "Operational",
        "temperature": 45.5,
        "vibration_score": 0.004,
        "current": 12.4,
        "voltage": 415.0,
        "sound": 75.2,
        "last_updated": current_time
    }

# --- RENDER SERVER BOOTSTRAP ---
if __name__ == "__main__":
    import uvicorn
    # Render assigns a specific port dynamically, we must listen to it
    port = int(os.environ.get("PORT", 8000))
    # 0.0.0.0 exposes the server to the public internet
    uvicorn.run(app, host="0.0.0.0", port=port)
