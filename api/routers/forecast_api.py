# flake8: noqa E501
"""ignore line limits"""

import os
import sys
import json
import logging
import asyncio
import aiofiles

from fastapi import FastAPI, APIRouter, HTTPException

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config import JSON_DIR
from prediction import run_prediction

router = APIRouter(prefix="/api/v1/forecast", tags=["Forecast"])

logger = logging.getLogger(__name__)

app = FastAPI()

logger.info(f"JSON_DIR resolved to: {JSON_DIR}")

"""
Forecast Analysis Endpoint
"""


@app.get("/{vehicle_id}/{model_type}")
async def get_forecast(vehicle_id: str, model_type: str):
    """
    Serve the forecast figure for a given vehicle and model type.
    """

    # Run sync prediction function in a thread to avoid blocking the event loop
    await asyncio.to_thread(run_prediction, vehicle_id=vehicle_id)

    forecast_path = os.path.join(
        JSON_DIR,
        vehicle_id,
        "forecast",
        f"{model_type.lower()}_forecast.json",
    )

    print(f" Path: {forecast_path}")

    if not os.path.exists(forecast_path):
        raise HTTPException(status_code=404, detail="Forecast not found")

    # Read JSON file asynchronously
    async with aiofiles.open(forecast_path, "r", encoding="utf-8") as f:
        content = await f.read()
        return json.loads(content)


@app.get("/info/{vehicle_id}/{model_type}")
async def get_forecast_info(vehicle_id: str, model_type: str):
    """
    Serve the forecast figure + summary info for a given vehicle and model type.
    """

    # Run prediction and gather data
    result = await asyncio.to_thread(run_prediction, vehicle_id=vehicle_id)

    forecast_path = os.path.join(
        JSON_DIR,
        vehicle_id,
        "forecast",
        f"{model_type.lower()}_forecast.json",
    )

    if not os.path.exists(forecast_path):
        raise HTTPException(status_code=404, detail="Forecast JSON file not found")

    async with aiofiles.open(forecast_path, "r", encoding="utf-8") as f:
        json_data = await f.read()
        forecast_figure = json.loads(json_data)

    return {
        "forecast_figure": forecast_figure,
        "forecast_info": result["forecast"],
        "summary": result["summary"],
    }
