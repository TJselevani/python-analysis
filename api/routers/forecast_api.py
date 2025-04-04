# flake8: noqa E501
"""ignore line limits"""

import os
import sys
import json

from fastapi import FastAPI
from fastapi import APIRouter, HTTPException

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config import JSON_DIR
from prediction import run_prediction

router = APIRouter(prefix="/api/v1/forecast", tags=["Forecast"])

app = FastAPI()

"""
Forecast Analysis Endpoint
"""


@app.get("/{vehicle_id}/{model_type}")
def get_forecast(vehicle_id: str, model_type: str):
    """
    Serve the forecast figure for a given vehicle and model type.
    """

    run_prediction(vehicle_id=vehicle_id)

    forecast_path = os.path.join(
        JSON_DIR,
        vehicle_id,
        "forecast",
        f"{model_type.lower()}_forecast.json",
    )

    print(f" Path: {forecast_path}")

    if not os.path.exists(forecast_path):
        raise HTTPException(status_code=404, detail="Forecast not found")

    with open(forecast_path, "r", encoding="utf-8") as f:
        return json.load(f)
