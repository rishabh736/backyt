import os
import random
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone

app = FastAPI(title="Yantra Kavach API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. OUR FAKE DATABASE (Memory)
machine_database = {
    "Yantra-01": {
        "machine_id": "Yantra-01",
        "temperature": 45.5,
        "vibration_score": 0.004,
        "current": 12.4,
        "sound": 75.2
    }
}

# The expected shape of data from ESP32
class SensorPayload(BaseModel):
    machine_id: str
    temperature: float
    vibration_score: float

# 2. CATCH THE ESP32 DATA AND SAVE IT TO THE DATABASE
@app.post("/api/upload-data")
async def receive_sensor_data(payload: SensorPayload):
    # Save or update the machine in our database dictionary
    machine_database[payload.machine_id] = {
        "machine_id": payload.machine_id,
        "temperature": payload.temperature,
        "vibration_score": payload.vibration_score,
        "current": 10.5, # Mock fallback
        "sound": 68.0    # Mock fallback
    }
    print(f"Saved to database: {payload.machine_id}")
    return {"status": "success"}

# 3. GIVE THE DASHBOARD ALL MACHINES IN THE DATABASE
@app.get("/api/machine-health")
async def get_machine_health():
    # Keep the simulator moving for Yantra-01
    machine_database["Yantra-01"]["temperature"] = 45.5 + random.uniform(-2.0, 3.5)
    machine_database["Yantra-01"]["vibration_score"] = 0.004 + random.uniform(-0.001, 0.003)
    
    # Return EVERYTHING in the database as a List (Array)
    return list(machine_database.values())

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
