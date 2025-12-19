# flake8: noqa E501
"""ignore line limits"""

import os
import sys
import json
from datetime import datetime
from fastapi import APIRouter, HTTPException, Query

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config import settings

router = APIRouter(prefix="/api/v1/eda/day", tags=["Day Analysis"])

"""
Utility Functions
"""


def validate_date(date: str):
    """Validates the format of the day string."""
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD."
        ) from exc


def get_precomputed_json(file_path: str):
    """Checks if the pre-computed JSON file exists and returns its content."""
    if not os.path.exists(file_path):
        raise HTTPException(
            status_code=404,
            detail="Data not found. Please run the pre-computation script.",
        )
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


"""
Day Analysis Endpoints
"""


@router.get("/sc_bundle")
def get_scatter_eda(
    date: str,
    vehicle_id: str = Query(
        None, description="Vehicle ID to filter results, leave empty for all vehicles"
    ),
):
    """
    Retrieve pre-computed day's scatter analysis for all vehicles or a specific vehicle.
    """
    validate_date(date)

    if vehicle_id:
        file_path = os.path.join(
            settings.JSON_DIR,
            vehicle_id,
            "eda",
            "day",
            f"day_scatter_earnings_{vehicle_id}_{date}.json",
        )
    else:
        file_path = os.path.join(
            settings.JSON_DIR, "all", "day", f"day_scatter_earnings_{date}.json"
        )

    return get_precomputed_json(file_path)
