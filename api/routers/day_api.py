# flake8: noqa E501
"""ignore line limits"""

import os
import sys
import json
import asyncio
import aiofiles
import logging
from datetime import datetime
from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Query

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from api.utils import log_and_handle_file_generation
from config import JSON_DIR
from scripts.day import (
    generate_day_earnings_with_scatter_bundle_plotly,
    generate_day_earnings_with_scatter_bundle_plotly_x1,
    generate_day_earnings_with_hourly_bundle_plotly,
    generate_day_earnings_with_week_bundle_plotly,
    generate_fare_trends_plotly,
    generate_fare_trends_plotly_x1,
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/eda/day", tags=["Day Analysis"])

logger.info(f"JSON_DIR resolved to: {JSON_DIR}")


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


async def generate_plot_json_async(
    file_path: str, generate_method: callable, *args, **kwargs
):
    logger.info(f"Checking if file exists: {file_path}")

    if not os.path.exists(file_path):
        logger.info(
            f"File not found. Generating file using method: {generate_method.__name__}"
        )
        try:
            await asyncio.to_thread(generate_method, *args, **kwargs)
        except Exception as e:
            logger.exception("Error during plot generation:")
            raise HTTPException(
                status_code=500, detail=f"Error during generation: {str(e)}"
            ) from e

        logger.info("Waiting for file to be created...")
        for _ in range(20):  # Wait for 2 seconds max
            if os.path.exists(file_path):
                logger.info(f"File found after waiting: {file_path}")
                break
            await asyncio.sleep(0.1)

    if not os.path.exists(file_path):
        logger.error(f"File not found after generation: {file_path}")
        raise HTTPException(
            status_code=500, detail="Generated file not found after execution"
        )

    try:
        async with aiofiles.open(file_path, mode="r", encoding="utf-8") as f:
            content = await f.read()
            logger.info(f"Successfully read file: {file_path}")
            return json.loads(content)
    except Exception as e:
        logger.exception(f"Failed to read generated file: {file_path}")
        raise HTTPException(status_code=500, detail=f"Error reading JSON file: {e}")


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
@log_and_handle_file_generation
async def get_scatter_eda(
    date: str,
    vehicle_id: str = Query(
        None, description="Vehicle ID to filter results, leave empty for all vehicles"
    ),
):
    logger.info(
        f"Received request for /sc_bundle with date={date}, vehicle_id={vehicle_id}"
    )

    validate_date(date)

    if vehicle_id:
        file = os.path.join(
            JSON_DIR,
            vehicle_id,
            "eda",
            "day",
            f"day_scatter_earnings_{vehicle_id}_{date}.json",
        )
        logger.info(f"Target file path for specific vehicle: {file}")

        def generate_day_eda_method():
            logger.info(
                "Calling generate_day_earnings_with_scatter_bundle_plotly_x1..."
            )
            generate_day_earnings_with_scatter_bundle_plotly_x1(
                date, vehicle_id, f"day_scatter_earnings_{vehicle_id}_{date}"
            )

    else:
        file = os.path.join(JSON_DIR, "all", "day", f"day_scatter_earnings_{date}.json")
        logger.info(f"Target file path for all vehicles: {file}")

        def generate_day_eda_method():
            logger.info("Calling generate_day_earnings_with_scatter_bundle_plotly...")
            generate_day_earnings_with_scatter_bundle_plotly(
                date, f"day_scatter_earnings_{date}"
            )

    try:
        response = await generate_plot_json_async(file, generate_day_eda_method)
        logger.info("Response successfully generated and returned.")
        return response
    except Exception as e:
        logger.exception("Exception occurred while generating day analysis.")
        raise HTTPException(
            status_code=500, detail=f"Error generating day analysis: {e}"
        )


@app.get("/hr_bundle")
async def get_hour_eda(
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
        return await generate_plot_json_async(file, generate_day_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating day - hour analysis: {e}"
        ) from e


@app.get("/wk_bundle")
async def get_week_eda(
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
        return await generate_plot_json_async(file, generate_day_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating day - week analysis: {e}"
        ) from e


@app.get("/trend")
async def get_trend_eda(
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
        return await generate_plot_json_async(file, generate_day_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating day trend analysis: {e}"
        ) from e
