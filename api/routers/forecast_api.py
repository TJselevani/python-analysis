# flake8: noqa E501
"""ignore line limits"""

import os
import sys
import json

from fastapi import APIRouter, HTTPException, Query

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config import settings
from prediction import run_prediction

router = APIRouter(prefix="/api/v1/forecast", tags=["Forecast"])

"""
Forecast Analysis Endpoint
"""


@router.get("/{vehicle_id}")
def get_forecast(
    vehicle_id: str,
    forecast_days: int = Query(30, description="Number of days to forecast"),
):
    """
    Retrieve the ensemble forecast for a given vehicle.
    """
    try:
        forecast_data = run_prediction(
            vehicle_id=vehicle_id, forecast_days=forecast_days
        )
        return forecast_data
    except FileNotFoundError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Model files not found in {settings.MODELS_DIR}. Please ensure models are trained by running `python train_models.py`. Details: {e}",
        ) from e
