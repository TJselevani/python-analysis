import os
import json
import plotly.graph_objects as go
from config import JSON_DIR


def plot_ensemble_forecast(historical_data, ensemble_df, vehicle_id):
    """
    Plot the ensemble forecast using Plotly and save as JSON.

    Parameters:
    - historical_data: Historical time series data (Pandas Series)
    - ensemble_df: DataFrame with ensemble forecast (must include 'date', 'ensemble_forecast', and other *_forecast columns)
    - vehicle_id: Vehicle ID for title
    """
    # Prepare JSON save directory
    json_save_dir = os.path.join(JSON_DIR, vehicle_id, "forecast")
    os.makedirs(json_save_dir, exist_ok=True)

    # Create Plotly figure
    fig = go.Figure()

    # Plot historical data
    fig.add_trace(
        go.Scatter(
            x=historical_data.index,
            y=historical_data.values,
            mode="lines",
            name="Historical Data",
            line=dict(color="black"),
        )
    )

    # Plot individual forecasts
    forecast_columns = [col for col in ensemble_df.columns if "forecast" in col]
    for col in forecast_columns:
        if col != "ensemble_forecast":
            fig.add_trace(
                go.Scatter(
                    x=ensemble_df["date"],
                    y=ensemble_df[col],
                    mode="lines",
                    name=col.replace("_forecast", ""),
                    opacity=0.5,
                )
            )

    # Plot ensemble forecast
    fig.add_trace(
        go.Scatter(
            x=ensemble_df["date"],
            y=ensemble_df["ensemble_forecast"],
            mode="lines",
            name="Ensemble Forecast",
            line=dict(color="red", width=3),
        )
    )

    # Update layout
    fig.update_layout(
        title=f"Ensemble Forecast for Vehicle {vehicle_id}",
        xaxis_title="Date",
        yaxis_title="Earnings (KSH)",
        template="plotly_white",
    )

    # fig.show()

    # Save JSON
    json_path = os.path.join(json_save_dir, "ensemble_forecast.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json.loads(fig.to_json()), f, indent=4)

    print(f"Ensemble forecast Plotly JSON saved at: {json_path}")
