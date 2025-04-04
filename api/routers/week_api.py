# flake8: noqa E501

import os
import sys
import json
from config import JSON_DIR
from fastapi import FastAPI
from fastapi import APIRouter, HTTPException, Query

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from scripts.week import (
    plot_weekly_fares_line,
    plot_weekly_fares_line_x1,
    plot_weekly_fares_bar,
    plot_weekly_fares_bar_x1,
    plot_weekly_total_revenue_bar,
    plot_weekly_total_revenue_line,
    plot_weekly_breakdown_by_vehicle,
)

router = APIRouter(prefix="/api/v1/eda/week", tags=["Week Analysis"])

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
Week Analysis Endpoints
"""

app = FastAPI()


@app.get("/trend/line")
def get_weekly_earnings_line_eda(
    vehicle_id: str = Query(
        None, description="Vehicle ID to filter results, leave empty for all vehicles"
    ),
):
    """
    Retrieve week's line graph analysis for all vehicles or a specific vehicle.
    - If `vehicle_id` is provided, fetch data for that vehicle.
    - If `vehicle_id` is not provided, fetch the combined data for all vehicles.
    """

    if vehicle_id:
        file = os.path.join(
            JSON_DIR,
            vehicle_id,
            "eda",
            "week",
            f"weekly_earnings_trend_line_{vehicle_id}.json",
        )

        def generate_week_eda_method():
            plot_weekly_fares_line_x1(
                vehicle_id, f"weekly_earnings_trend_line_{vehicle_id}"
            )

    else:
        file = os.path.join(JSON_DIR, "all", "week", "weekly_earnings_trend_line.json")

        def generate_week_eda_method():
            plot_weekly_fares_line("weekly_earnings_trend_line")

    try:
        return generate_plot_json(file, generate_week_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating weekly earnings line analysis: {e}",
        ) from e


@app.get("/trend/bar")
def get_weekly_earnings_bar_eda(
    vehicle_id: str = Query(
        None, description="Vehicle ID to filter results, leave empty for all vehicles"
    ),
):
    """
    Retrieve day's bar graph analysis for all vehicles or a specific vehicle.
    - If `vehicle_id` is provided, fetch data for that vehicle.
    - If `vehicle_id` is not provided, fetch the combined data for all vehicles.
    """

    if vehicle_id:
        file = os.path.join(
            JSON_DIR,
            vehicle_id,
            "eda",
            "week",
            f"weekly_earnings_trend_bar_{vehicle_id}.json",
        )

        def generate_week_eda_method():
            plot_weekly_fares_bar_x1(
                vehicle_id, f"weekly_earnings_trend_bar_{vehicle_id}"
            )

    else:
        file = os.path.join(JSON_DIR, "all", "week", "weekly_earnings_trend_bar.json")

        def generate_week_eda_method():
            plot_weekly_fares_bar("weekly_earnings_trend_bar")

    try:
        return generate_plot_json(file, generate_week_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating weekly earnings bar analysis: {e}",
        ) from e


@app.get("/revenue")
def get_weekly_total_eda(
    bar: str = Query(None, description="to filter results, leave empty for default"),
):
    """
    Retrieve weeks's revenue analysis for all vehicles.
    - If `bar` is provided, fetch bar data.
    - If `bar` is not provided, fetch the line data.
    """

    if bar:
        file = os.path.join(
            JSON_DIR,
            "all",
            "week",
            "weekly_total_earnings_line.json",
        )

        def generate_day_eda_method():
            plot_weekly_total_revenue_bar("weekly_total_earnings_bar")

    else:
        file = os.path.join(JSON_DIR, "all", "week", "weekly_total_earnings_line.json")

        def generate_day_eda_method():
            plot_weekly_total_revenue_line("weekly_total_earnings_line")

    try:
        return generate_plot_json(file, generate_day_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating weekly total eda analysis: {e}"
        ) from e


@app.get("/wk_bundle")
def get_week_eda():
    """
    Retrieve Combined view showing weekly breakdown by vehicle and total.
    """
    scatter_file = os.path.join(JSON_DIR, "all", "week", "week_bundled_earnings.json")

    def generate_day_eda_method():
        plot_weekly_breakdown_by_vehicle("_week_bundled_earnings")

    try:
        return generate_plot_json(scatter_file, generate_day_eda_method)
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error generating day analysis: {e}"
        ) from e
