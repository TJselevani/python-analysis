# flake8: noqa E501
"""Forecast endpoints with decomposition support and improved file handling."""

import os
import sys
import json
import logging
import asyncio
import aiofiles

from fastapi import APIRouter, HTTPException, Query

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config import JSON_DIR
from predict import run_prediction

router = APIRouter(prefix="/api/v1/forecast", tags=["Forecast"])
logger = logging.getLogger(__name__)

"""
Utility Function
"""


async def load_or_generate_json(file_path: str, generate_fn: callable, *args, **kwargs):
    """Checks if a file exists. If not, runs the generator method and reads the file."""
    if not os.path.exists(file_path):
        await asyncio.to_thread(generate_fn, *args, **kwargs)

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"File not found at {file_path}")

    async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
        return json.loads(await f.read())


"""
Forecast Endpoints
"""


@router.get("/{vehicle_id}/{model_type}")
async def get_forecast(vehicle_id: str, model_type: str):
    """
    Serve the forecast figure for a given vehicle and model type.
    If not found, will run prediction first.
    """
    model_type = model_type.lower()
    forecast_path = os.path.join(
        JSON_DIR, vehicle_id, "forecast", f"{model_type}_forecast.json"
    )

    return await load_or_generate_json(
        forecast_path, run_prediction, vehicle_id=vehicle_id
    )


@router.get("/info/{vehicle_id}/{model_type}")
async def get_forecast_info(vehicle_id: str, model_type: str):
    """
    Serve the forecast + summary info for a given vehicle and model type.
    Will run prediction before returning.
    """
    model_type = model_type.lower()
    result = await asyncio.to_thread(run_prediction, vehicle_id=vehicle_id)

    forecast_path = os.path.join(
        JSON_DIR, vehicle_id, "forecast", f"{model_type}_forecast.json"
    )
    forecast_figure = await load_or_generate_json(
        forecast_path, run_prediction, vehicle_id=vehicle_id
    )

    return {
        "forecast_figure": forecast_figure,
        "forecast_info": result["forecast"],
        "summary": result["summary"],
    }


"""
Decomposition Endpoint
"""


@router.get("/decomposition/{vehicle_id}")
async def get_decomposition_data(
    vehicle_id: str,
    component: str = Query(..., enum=["observed", "trend", "seasonality", "residuals"]),
):
    """
    Serve decomposition data for a given vehicle and time series component.
    - Components: observed, trend, seasonality, residuals
    - File path: json/{vehicle_id}/decomposition/{component}.json
    """
    file_path = os.path.join(JSON_DIR, vehicle_id, "decomposition", f"{component}.json")

    return await load_or_generate_json(
        file_path, run_prediction, vehicle_id=vehicle_id
    )

    # if not os.path.exists(file_path):
    #     raise HTTPException(
    #         status_code=404,
    #         detail=f"Decomposition file '{component}.json' not found for vehicle {vehicle_id}",
    #     )

    # async with aiofiles.open(file_path, "r", encoding="utf-8") as f:
    #     return json.loads(await f.read())
