import os
import json
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
from config import FILES_DIR, JSON_DIR


def plot_forecast(historical_data, forecast_df, vehicle_id, model_type):
    """
    Plot the historical data and forecast.
    Save as a JSON file for Angular consumption.
    """
    # Ensure save directory exists
    forecast_json_save_dir = os.path.join("json", vehicle_id, "forecast")
    os.makedirs(forecast_json_save_dir, exist_ok=True)

    # Create Plotly figure
    fig = go.Figure()

    # Convert historical data to Python-native types
    historical_x = historical_data.index.tolist()
    historical_y = [
        float(y) if isinstance(y, (np.float64, np.float32, int)) else y
        for y in historical_data.values.tolist()
    ]

    # Add historical data
    fig.add_trace(
        go.Scatter(
            x=historical_x,
            y=historical_y,
            mode="lines",
            name="Historical Data",
            line=dict(color="blue"),
        )
    )

    # Add forecast data (with type handling)
    if isinstance(forecast_df, pd.DataFrame) and "date" in forecast_df.columns:
        forecast_x = [
            str(date) if isinstance(date, np.datetime64) else date
            for date in forecast_df["date"].tolist()
        ]
        forecast_y = [
            float(y) if isinstance(y, (np.float64, np.float32, int)) else y
            for y in forecast_df["earnings"].tolist()
        ]
        fig.add_trace(
            go.Scatter(
                x=forecast_x,
                y=forecast_y,
                mode="lines",
                name="Forecast",
                line=dict(color="red"),
            )
        )

    # Update layout
    fig.update_layout(
        title=f"{model_type} Forecast for Vehicle {vehicle_id}",
        xaxis_title="Date",
        yaxis_title="Earnings (KSH)",
        template="plotly_white",
        autosize=True,
        margin=dict(l=50, r=50, b=100, t=100),
    )

    # Convert dates to ISO strings before saving
    def convert_dates(obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        return obj

    fig_json = json.loads(json.dumps(fig.to_plotly_json(), default=convert_dates))

    # Save JSON file
    json_file_path = os.path.join(
        forecast_json_save_dir, f"{model_type.lower()}_forecast.json"
    )
    with open(json_file_path, "w") as json_file:
        json.dump(fig_json, json_file, indent=4)

    print(f"Plotly JSON saved at: {json_file_path}")
    return fig_json


def plot_prophet_forecast(historical_data, model, forecast, vehicle_id, model_type):
    """
    Plot the Prophet forecast.
    Generate a Plotly figure for the historical data and forecast.

    Parameters:
    - model: Trained Prophet model
    - forecast: Forecast DataFrame from Prophet
    - vehicle_id: Vehicle ID for the title
    - model_type: Type of model used (Prophet etc.)
    """
    # Define directory paths
    analysis_save_dir = os.path.join(FILES_DIR, vehicle_id, "analysis")
    forecast_save_dir = os.path.join(FILES_DIR, vehicle_id, "forecast")

    # Ensure directories exist
    os.makedirs(analysis_save_dir, exist_ok=True)
    os.makedirs(forecast_save_dir, exist_ok=True)

    """
    saving PNG forecast
    """

    plt.figure(figsize=(16, 12))

    # Plot the forecast
    model.plot(forecast)
    plt.title(f"{model_type} Forecast for Vehicle {vehicle_id}")
    plt.xlabel("Date")
    plt.ylabel("Earnings (KSH)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(
        os.path.join(forecast_save_dir, f"{model_type.lower()}_forecast.png"), dpi=300
    )
    plt.show()

    # Plot the components of the forecast
    model.plot_components(forecast)
    plt.title(f"{model_type} Forecast Components for Vehicle {vehicle_id}")
    plt.xlabel("Date")
    plt.ylabel("Earnings (KSH)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig(os.path.join(analysis_save_dir, "time_series_components.png"), dpi=300)
    plt.show()

    """
    Saving JSON forecast
    """

    # Define JSON directory paths
    analysis_json_save_dir = os.path.join(JSON_DIR, vehicle_id, "analysis")
    forecast_json_save_dir = os.path.join(JSON_DIR, vehicle_id, "forecast")

    # Ensure JSON directories exist
    os.makedirs(analysis_json_save_dir, exist_ok=True)
    os.makedirs(forecast_json_save_dir, exist_ok=True)

    # Convert forecast DataFrame to JSON
    forecast_json = forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].to_json(
        orient="records", date_format="iso"
    )

    # Save JSON to file
    json_file_path = os.path.join(
        forecast_json_save_dir, f"{model_type.lower()}_forecast.json"
    )
    with open(json_file_path, "w") as json_file:
        json.dump(json.loads(forecast_json), json_file, indent=4)

    print(f"Forecast saved to {json_file_path}")

    return forecast_json  # Optionally return JSON data


def create_dummy_plotly_json():
    """
    Create a dummy Plotly graph and save it as JSON.
    """
    # Create dummy data
    dates = pd.date_range("2024-01-01", periods=30).tolist()
    values = [np.random.randint(100, 500) for _ in range(30)]

    # Create Plotly figure
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=dates,
            y=values,
            mode="lines+markers",
            name="Dummy Data",
            line=dict(color="blue"),
            marker=dict(color="red"),
        )
    )

    # Update layout
    fig.update_layout(
        title="Dummy Forecast Example",
        xaxis_title="Date",
        yaxis_title="Value",
        template="plotly_dark",
        autosize=True,
        margin=dict(l=50, r=50, b=100, t=100),
    )

    # Convert dates to ISO strings and save JSON
    def convert_dates(obj):
        if isinstance(obj, pd.Timestamp):
            return obj.isoformat()
        return obj

    # Save directory setup
    save_dir = os.path.join("json", "dummy")
    os.makedirs(save_dir, exist_ok=True)

    # Convert and save JSON
    fig_json = json.loads(json.dumps(fig.to_plotly_json(), default=convert_dates))
    json_file_path = os.path.join(save_dir, "dummy_plot.json")

    with open(json_file_path, "w") as json_file:
        json.dump(fig_json, json_file, indent=4)

    print(f"Dummy Plotly JSON saved at: {json_file_path}")
    return fig_json
