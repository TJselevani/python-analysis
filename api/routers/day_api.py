# flake8: noqa E501
"""ignore line limits"""

import os
import sys
import json
from datetime import datetime
from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Query

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config import JSON_DIR
from scripts.day import (
    generate_day_earnings_with_scatter_bundle_plotly,
    generate_day_earnings_with_scatter_bundle_plotly_x1,
    generate_day_earnings_with_hourly_bundle_plotly,
    generate_day_earnings_with_week_bundle_plotly,
    generate_fare_trends_plotly,
    generate_fare_trends_plotly_x1,
)

router = APIRouter(prefix="/api/v1/eda/day", tags=["Day Analysis"])

"""
Utility Functions
"""


def validate_date(date: str):
    """validates the format of the day string"""
    try:
        datetime.strptime(date, "%Y-%m-%d")
    except ValueError as exc:  # Capture the exception as `exc`
        raise HTTPException(
            status_code=400, detail="Invalid date format. Use YYYY-MM-DD."
        ) from exc  # Explicitly re-raise from the original exception


def generate_plot_json(file_path: str, generate_method: callable, *args, **kwargs):
    """Checks if the file exists, and if not, generates it by calling the respective method."""
    if not os.path.exists(file_path):
        # Call the method to generate the file
        generate_method(*args, **kwargs)
        print(f"Generated {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


app = FastAPI()

"""
Day Analysis Endpoints
"""


@app.get("/sc_bundle")
def get_scatter_eda(
    date: str,
    vehicle_id: str = Query(
        None, description="Vehicle ID to filter results, leave empty for all vehicles"
    ),
):
    """
    Retrieve day's scatter analysis for all vehicles or a specific vehicle.
    - If `vehicle_id` is provided, fetch data for that vehicle.
    - If `vehicle_id` is not provided, fetch the combined data for all vehicles.
    """

    # Validate date format to avoid parsing issues
    validate_date(date)

    if vehicle_id:
        file = os.path.join(
            JSON_DIR,
            vehicle_id,
            "eda",
            "day",
            f"day_scatter_earnings_{vehicle_id}_{date}.json",
        )

        def generate_day_eda_method():
            generate_day_earnings_with_scatter_bundle_plotly_x1(
                date, vehicle_id, f"day_scatter_earnings_{vehicle_id}_{date}"
            )

    else:
        file = os.path.join(JSON_DIR, "all", "day", f"day_scatter_earnings_{date}.json")

        def generate_day_eda_method():
            generate_day_earnings_with_scatter_bundle_plotly(
                f"{date}", f"day_scatter_earnings_{date}"
            )

    try:
        return generate_plot_json(file, generate_day_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating day analysis: {e}"
        ) from e


@app.get("/hr_bundle")
def get_hour_eda(
    date: str,
    vehicle_id: str = Query(
        None, description="Vehicle ID to filter results, leave empty for all vehicles"
    ),
):
    """
    Retrieve day's hourly analysis for all vehicles or a specific vehicle.
    - If `vehicle_id` is provided, fetch data for that vehicle.
    - If `vehicle_id` is not provided, fetch the combined data for all vehicles.
    """

    # Validate date format to avoid parsing issues
    validate_date(date)

    if vehicle_id:
        file = os.path.join(
            JSON_DIR, vehicle_id, "eda", "day", f"day_hour_bundled_earnings_{date}.json"
        )

        def generate_day_eda_method():
            generate_day_earnings_with_hourly_bundle_plotly(
                date, f"day_hour_bundled_earnings_{date}"
            )

    else:
        file = os.path.join(
            JSON_DIR, "all", "day", f"day_hour_bundled_earnings_{date}.json"
        )

        def generate_day_eda_method():
            generate_day_earnings_with_hourly_bundle_plotly(
                date, f"day_hour_bundled_earnings_{date}"
            )

    try:
        return generate_plot_json(file, generate_day_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating day - hour analysis: {e}"
        ) from e


@app.get("/wk_bundle")
def get_week_eda(
    date: str,
    vehicle_id: str = Query(
        None, description="Vehicle ID to filter results, leave empty for all vehicles"
    ),
):
    """
    Retrieve day scatter analysis for all vehicles or a specific vehicle.
    - If `vehicle_id` is provided, fetch data for that vehicle.
    - If `vehicle_id` is not provided, fetch the combined data for all vehicles.
    """

    # Validate date format to avoid parsing issues
    validate_date(date)

    if vehicle_id:
        file = os.path.join(
            JSON_DIR, vehicle_id, "eda", "day", f"day_week_bundled_earnings_{date}.json"
        )

        def generate_day_eda_method():
            generate_day_earnings_with_week_bundle_plotly(
                date, f"day_week_bundled_earnings_{date}"
            )

    else:
        file = os.path.join(
            JSON_DIR, "all", "day", f"day_week_bundled_earnings_{date}.json"
        )

        def generate_day_eda_method():
            generate_day_earnings_with_week_bundle_plotly(
                f"{date}", f"day_week_bundled_earnings_{date}"
            )

    try:
        return generate_plot_json(file, generate_day_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating day - week analysis: {e}"
        ) from e


@app.get("/trend")
def get_trend_eda(
    vehicle_id: str = Query(
        None, description="Vehicle ID to filter results, leave empty for all vehicles"
    ),
):
    """
    Retrieve date trend analysis for all vehicles or a specific vehicle.
    - If `vehicle_id` is provided, fetch data for that vehicle.
    - If `vehicle_id` is not provided, fetch the combined data for all vehicles.
    """

    if vehicle_id:
        file = os.path.join(
            JSON_DIR, vehicle_id, "eda", "day", "daily_fare_trends.json"
        )

        def generate_day_eda_method():
            generate_fare_trends_plotly_x1(vehicle_id, "daily_fare_trends")

    else:
        file = os.path.join(JSON_DIR, "all", "day", "daily_fare_trends.json")

        def generate_day_eda_method():
            generate_fare_trends_plotly("daily_fare_trends")

    try:
        return generate_plot_json(file, generate_day_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating day trend analysis: {e}"
        ) from e
