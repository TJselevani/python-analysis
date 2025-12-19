# flake8: noqa E501
import os
import json
import pandas as pd
import numpy as np

# Define unique colors for each vehicle, plus "Unknown" and "Failed Transactions"
VEHICLE_COLORS = {
    "SM191": "blue",
    "SM192": "green",
    "SM944": "yellow",
    "SM055": "purple",
    "SM024": "orange",
    "Unknown": "gray",
    "Failed": "red",
}


def load_and_prepare_data(csv_path):
    """Loads the CSV data and prepares the necessary columns."""
    data = pd.read_csv(csv_path)
    data["created_at"] = pd.to_datetime(data["created_at"])
    data["date"] = data["created_at"].dt.date
    data["minutes"] = data["created_at"].dt.hour * 60 + data["created_at"].dt.minute
    data["color"] = data["vehicle_booked"].map(VEHICLE_COLORS).fillna("gray")
    data.loc[data["payment_status"] == 3, "color"] = "red"
    data = data[data["transaction_type"] == "CREDIT"].copy()
    return data


def generate_day_scatter_json(data, date_str, output_dir, vehicle_id=None):
    """
    Generates a JSON file with data for a daily scatter plot of transactions.
    """
    specific_date = pd.to_datetime(date_str).date()
    day_data = data[data["date"] == specific_date]

    if vehicle_id:
        day_data = day_data[day_data["vehicle_booked"] == vehicle_id]
        output_path = os.path.join(
            output_dir,
            vehicle_id,
            "eda",
            "day",
            f"day_scatter_earnings_{vehicle_id}_{date_str}.json",
        )
    else:
        output_path = os.path.join(
            output_dir, "all", "day", f"day_scatter_earnings_{date_str}.json"
        )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    plot_data = {
        "title": f"Scatter Plot of Transactions ({date_str}) - {vehicle_id or 'All Vehicles'}",
        "x_axis_label": "Time (Minutes in Day)",
        "y_axis_label": "Transaction Amount (Ksh)",
        "series": [
            {
                "name": vehicle_id or "Transactions",
                "x": day_data["minutes"].tolist(),
                "y": day_data["amount"].tolist(),
                "color": day_data["color"].tolist(),
                "type": "scatter",
            }
        ],
    }

    with open(output_path, "w") as f:
        json.dump(plot_data, f, indent=4)
    print(f"Generated JSON: {output_path}")
