import os
import json
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
from config import JSON_DIR


def plot_forecast(historical_data, forecast_df, vehicle_id, model_type):
    """
    Plot the historical data and forecast.
    Save as a JSON file for Angular consumption.
    """
    # Ensure save directory exists
    forecast_json_save_dir = os.path.join(JSON_DIR, vehicle_id, "forecast")
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

    # fig.show()

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

    print(f"{model_type} Plotly forecast JSON saved at: {json_file_path}")
    # return fig_json


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
    fig = go.Figure()

    # Historical Data
    fig.add_trace(
        go.Scatter(
            x=historical_data.index,
            y=historical_data.values,
            mode="lines",
            name="Historical Data",
            line=dict(color="blue"),
        )
    )

    # Forecast (yhat)
    fig.add_trace(
        go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat"],
            mode="lines",
            name="Forecast",
            line=dict(color="red"),
        )
    )

    # Confidence Interval (optional)
    fig.add_trace(
        go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat_upper"],
            mode="lines",
            name="Upper Bound",
            line=dict(color="rgba(255,0,0,0.3)"),
            showlegend=False,
        )
    )

    fig.add_trace(
        go.Scatter(
            x=forecast["ds"],
            y=forecast["yhat_lower"],
            mode="lines",
            name="Lower Bound",
            fill="tonexty",  # fill area between lower and upper
            fillcolor="rgba(255,0,0,0.1)",
            line=dict(color="rgba(255,0,0,0.3)"),
            showlegend=False,
        )
    )

    fig.update_layout(
        title=f"{model_type} Forecast for Vehicle {vehicle_id}",
        xaxis_title="Date",
        yaxis_title="Earnings (KSH)",
        template="plotly_white",
    )

    # fig.show()

    # Define JSON directory paths
    analysis_json_save_dir = os.path.join(JSON_DIR, vehicle_id, "analysis")
    forecast_json_save_dir = os.path.join(JSON_DIR, vehicle_id, "forecast")

    # Ensure JSON directories exist
    os.makedirs(analysis_json_save_dir, exist_ok=True)
    os.makedirs(forecast_json_save_dir, exist_ok=True)

    # Save Plotly chart as JSON
    plotly_json = fig.to_plotly_json()

    json_file_path = os.path.join(
        forecast_json_save_dir, f"{model_type.lower()}_forecast.json"
    )
    with open(json_file_path, "w", encoding="utf-8") as f:
        json.dump(plotly_json, f, indent=4, cls=PlotlyJSONEncoder)

    print(f"{model_type} Plotly forecast JSON saved at: {json_file_path}")
    # return forecast_json  # Optionally return JSON data
