# flake8: noqa E501

import os
import sys
import json
from config import JSON_DIR
from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Query

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scripts.month import (
    plot_monthly_fares_line,
    plot_monthly_fares_line_x1,
    plot_monthly_fares_bar,
    plot_monthly_fares_bar_x1,
    plot_monthly_total_revenue_bar,
    plot_monthly_total_revenue_line,
    plot_monthly_breakdown_by_vehicle,
)

router = APIRouter(prefix="/api/v1/eda/month", tags=["Month Analysis"])

"""
Utility Functions
"""


def generate_plot_json(file_path: str, generate_method: callable, *args, **kwargs):
    """Checks if the file exists, and if not, generates it by calling the respective method."""
    if not os.path.exists(file_path):
        # Call the method to generate the file
        generate_method(*args, **kwargs)
        print(f"Generated {file_path}")
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)


"""
Month Analysis Endpoints
"""

app = FastAPI()


@app.get("/trend/line")
def get_monthly_earnings_line_eda(
    vehicle_id: str = Query(
        None, description="Vehicle ID to filter results, leave empty for all vehicles"
    ),
):
    """
    Retrieve months's line graph analysis for all vehicles or a specific vehicle.
    - If `vehicle_id` is provided, fetch data for that vehicle.
    - If `vehicle_id` is not provided, fetch the combined data for all vehicles.
    """

    if vehicle_id:
        file = os.path.join(
            JSON_DIR,
            vehicle_id,
            "eda",
            "month",
            f"monthly_earnings_trend_line_{vehicle_id}.json",
        )

        def generate_week_eda_method():
            plot_monthly_fares_line_x1(
                vehicle_id, f"monthly_earnings_trend_line_{vehicle_id}"
            )

    else:
        file = os.path.join(
            JSON_DIR, "all", "month", "monthly_earnings_trend_line.json"
        )

        def generate_week_eda_method():
            plot_monthly_fares_line("monthly_earnings_trend_line")

    try:
        return generate_plot_json(file, generate_week_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating monthly earnings line analysis: {e}",
        ) from e


@app.get("/trend/bar")
def get_weekly_earnings_bar_eda(
    vehicle_id: str = Query(
        None, description="Vehicle ID to filter results, leave empty for all vehicles"
    ),
):
    """
    Retrieve month's bar graph analysis for all vehicles or a specific vehicle.
    - If `vehicle_id` is provided, fetch data for that vehicle.
    - If `vehicle_id` is not provided, fetch the combined data for all vehicles.
    """

    if vehicle_id:
        file = os.path.join(
            JSON_DIR,
            vehicle_id,
            "eda",
            "month",
            f"monthly_earnings_trend_bar_{vehicle_id}.json",
        )

        def generate_week_eda_method():
            plot_monthly_fares_bar_x1(
                vehicle_id, f"monthly_earnings_trend_bar_{vehicle_id}"
            )

    else:
        file = os.path.join(JSON_DIR, "all", "month", "monthly_earnings_trend_bar.json")

        def generate_week_eda_method():
            plot_monthly_fares_bar("monthly_earnings_trend_bar")

    try:
        return generate_plot_json(file, generate_week_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating monthly earnings bar analysis: {e}",
        ) from e


@app.get("/revenue")
def get_monthly_total_eda(
    bar: str = Query(None, description="to filter results, leave empty for default"),
):
    """
    Retrieve month's revenue analysis for all vehicles.
    - If `bar` is provided, fetch bar data.
    - If `bar` is not provided, fetch the line data.
    """

    if bar:
        file = os.path.join(
            JSON_DIR,
            "all",
            "month",
            "monthly_total_earnings_line.json",
        )

        def generate_day_eda_method():
            plot_monthly_total_revenue_bar("monthly_total_earnings_bar")

    else:
        file = os.path.join(
            JSON_DIR, "all", "month", "monthly_total_earnings_line.json"
        )

        def generate_day_eda_method():
            plot_monthly_total_revenue_line("monthly_total_earnings_line")

    try:
        return generate_plot_json(file, generate_day_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating monthly total eda analysis: {e}"
        ) from e


@app.get("/mt_bundle")
def get_month_eda():
    """
    Retrieve Combined view showing weekly breakdown by vehicle and total.
    """
    scatter_file = os.path.join(
        JSON_DIR, "all", "month", "monthly_bundled_earnings.json"
    )

    def generate_day_eda_method():
        plot_monthly_breakdown_by_vehicle("monthly_bundled_earnings")

    try:
        return generate_plot_json(scatter_file, generate_day_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating month eda analysis: {e}"
        ) from e
