# flake8: noqa E501
# flake8: noqa C0413
"""ignore line limits"""

import os
import sys
import json
import asyncio
import logging
import aiofiles

from fastapi import APIRouter, HTTPException, Query

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config import JSON_DIR
from scripts.month import (
    plot_monthly_fares_line,
    plot_monthly_fares_line_x1,
    plot_monthly_fares_bar,
    plot_monthly_fares_bar_x1,
    plot_monthly_total_revenue_bar,
    plot_monthly_total_revenue_line,
    plot_monthly_breakdown_by_vehicle,
)

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/eda/month", tags=["Month Analysis"])

"""
Utility Function
"""


async def generate_plot_json_async(
    file_path: str, generate_method: callable, *args, **kwargs
):
    """Asynchronously returns the JSON file content if available or generates it if missing."""
    if not os.path.exists(file_path):
        logger.debug(f"File not found. Generating via: {generate_method.__name__}")
        try:
            await asyncio.to_thread(generate_method, *args, **kwargs)
        except Exception as e:
            logger.exception("Plot generation failed:")
            raise HTTPException(
                status_code=500, detail=f"Generation failed: {e}"
            ) from e

        logger.info("Waiting for file creation...")
        for _ in range(20):  # Wait max 2 seconds
            if os.path.exists(file_path):
                break
            await asyncio.sleep(0.1)

    if not os.path.exists(file_path):
        logger.error(f"File not found after generation: {file_path}")
        raise HTTPException(status_code=500, detail="File not found post-generation")

    try:
        async with aiofiles.open(file_path, mode="r", encoding="utf-8") as f:
            return json.loads(await f.read())
    except Exception as e:
        logger.exception("Error reading JSON:")
        raise HTTPException(status_code=500, detail=f"Error reading JSON: {e}") from e


"""
Endpoints
"""


@router.get("/trend/line")
async def get_monthly_earnings_line_eda(
    vehicle_id: str = Query(
        None, description="Vehicle ID to filter results, leave empty for all vehicles"
    ),
):
    """Monthly line graph analysis."""
    if vehicle_id:
        file = os.path.join(
            JSON_DIR,
            vehicle_id,
            "eda",
            "month",
            f"monthly_earnings_trend_line_{vehicle_id}.json",
        )

        def generate_method():
            plot_monthly_fares_line_x1(
                vehicle_id, f"monthly_earnings_trend_line_{vehicle_id}"
            )

    else:
        file = os.path.join(
            JSON_DIR, "all", "month", "monthly_earnings_trend_line.json"
        )

        def generate_method():
            plot_monthly_fares_line("monthly_earnings_trend_line")

    return await generate_plot_json_async(file, generate_method)


@router.get("/trend/bar")
async def get_monthly_earnings_bar_eda(
    vehicle_id: str = Query(
        None, description="Vehicle ID to filter results, leave empty for all vehicles"
    ),
):
    """Monthly bar graph analysis."""
    if vehicle_id:
        file = os.path.join(
            JSON_DIR,
            vehicle_id,
            "eda",
            "month",
            f"monthly_earnings_trend_bar_{vehicle_id}.json",
        )

        def generate_method():
            plot_monthly_fares_bar_x1(
                vehicle_id, f"monthly_earnings_trend_bar_{vehicle_id}"
            )

    else:
        file = os.path.join(JSON_DIR, "all", "month", "monthly_earnings_trend_bar.json")

        def generate_method():
            plot_monthly_fares_bar("monthly_earnings_trend_bar")

    return await generate_plot_json_async(file, generate_method)


@router.get("/mt_bundle")
async def get_month_eda():
    """Combined view showing monthly breakdown by vehicle."""
    file = os.path.join(JSON_DIR, "all", "month", "monthly_bundled_earnings.json")

    def generate_method():
        plot_monthly_breakdown_by_vehicle("monthly_bundled_earnings")

    return await generate_plot_json_async(file, generate_method)


@router.get("/trend")
async def get_monthly_total_eda(
    bar: str = Query(
        None,
        description="Include ?bar=true to get bar chart, otherwise line chart is returned.",
    ),
):
    """Monthly total revenue trend, either bar or line."""
    if bar:
        file = os.path.join(JSON_DIR, "all", "month", "monthly_total_earnings_bar.json")

        def generate_method():
            plot_monthly_total_revenue_bar("monthly_total_earnings_bar")

    else:
        file = os.path.join(
            JSON_DIR, "all", "month", "monthly_total_earnings_line.json"
        )

        def generate_method():
            plot_monthly_total_revenue_line("monthly_total_earnings_line")

    return await generate_plot_json_async(file, generate_method)
