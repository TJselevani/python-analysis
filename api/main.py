from fastapi import FastAPI, HTTPException
import os
import sys
import json

from fastapi.middleware.cors import CORSMiddleware

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import JSON_DIR

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/v1/forecast/{vehicle_id}/{model_type}")
def get_forecast(vehicle_id: str, model_type: str):
    """
    Serve the forecast figure for a given vehicle and model type.
    """
    forecast_path = os.path.join(
        JSON_DIR, vehicle_id, "forecast", f"{model_type.lower()}_forecast.json"
    )

    if os.path.exists(forecast_path):
        with open(forecast_path, "r") as f:
            # Directly return the JSON data
            return json.load(f)
    else:
        raise HTTPException(status_code=404, detail="Forecast not found")
