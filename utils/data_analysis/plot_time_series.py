import os
import json
import matplotlib.pyplot as plt
from config import FILES_DIR, JSON_DIR
from utils.data_analysis.analyze_time_series import analyze_time_series
import plotly.graph_objects as go


def plot_time_series_analysis(ts_data, vehicle_id):
    """
    Plot the time series data and its components.
    Generate Plotly time series analysis and save it as JSON.

    Parameters:
    - ts_data: Time series data
    - vehicle_id: Vehicle ID for title
    """
    # Define directory paths
    save_dir = os.path.join(FILES_DIR, vehicle_id, "analysis")
    os.makedirs(save_dir, exist_ok=True)

    # Define JSON directory paths
    save_dir = os.path.join(JSON_DIR, vehicle_id, "analysis")
    os.makedirs(save_dir, exist_ok=True)

    """
    Save PNG time series analysis
    """
    plt.figure(figsize=(14, 12))

    # Plot the original time series
    plt.subplot(2, 1, 1)
    plt.plot(ts_data.index, ts_data.values)
    plt.title(f"Time Series Analysis on Daily Earnings for Vehicle {vehicle_id}")
    plt.ylabel("Amount (KSH)")
    plt.grid(True)

    # Try to plot the decomposition if we have enough data
    decomposition = analyze_time_series(ts_data)
    if decomposition:
        plt.figure(figsize=(16, 12))
        plt.subplot(4, 1, 1)
        plt.plot(decomposition.observed)
        plt.title("Observed")
        plt.grid(True)

        plt.subplot(4, 1, 2)
        plt.plot(decomposition.trend)
        plt.title("Trend")
        plt.grid(True)

        plt.subplot(4, 1, 3)
        plt.plot(decomposition.seasonal)
        plt.title("Seasonality")
        plt.grid(True)

        plt.subplot(4, 1, 4)
        plt.plot(decomposition.resid)
        plt.title("Residuals")
        plt.grid(True)

        plt.tight_layout()
        plt.savefig(os.path.join(save_dir, "time_series_decomposition.png"), dpi=300)

    plt.tight_layout()
    plt.savefig(os.path.join(save_dir, "time_series_analysis.png"), dpi=300)

    """
    Save JSON time series analysis
    """

    # Create a main figure for the original time series
    fig_main = go.Figure()
    fig_main.add_trace(
        go.Scatter(
            x=ts_data.index, y=ts_data.values, mode="lines", name="Daily Earnings"
        )
    )

    fig_main.update_layout(
        title=f"Time Series Analysis on Daily Earnings for Vehicle {vehicle_id}",
        xaxis_title="Date",
        yaxis_title="Amount (KSH)",
        template="plotly_dark",
    )

    # Initialize JSON output
    json_output = {"time_series_analysis": json.loads(fig_main.to_json())}

    # Try to analyze the time series decomposition
    decomposition = analyze_time_series(ts_data)
    if decomposition:
        fig_decomposition = go.Figure()

        # Observed
        fig_decomposition.add_trace(
            go.Scatter(
                x=ts_data.index, y=decomposition.observed, mode="lines", name="Observed"
            )
        )

        # Trend
        fig_decomposition.add_trace(
            go.Scatter(
                x=ts_data.index, y=decomposition.trend, mode="lines", name="Trend"
            )
        )

        # Seasonality
        fig_decomposition.add_trace(
            go.Scatter(
                x=ts_data.index,
                y=decomposition.seasonal,
                mode="lines",
                name="Seasonality",
            )
        )

        # Residuals
        fig_decomposition.add_trace(
            go.Scatter(
                x=ts_data.index, y=decomposition.resid, mode="lines", name="Residuals"
            )
        )

        fig_decomposition.update_layout(
            title="Time Series Decomposition",
            xaxis_title="Date",
            yaxis_title="Value",
            template="plotly_dark",
        )

        # Add decomposition chart to JSON output
        json_output["time_series_decomposition"] = json.loads(
            fig_decomposition.to_json()
        )

    # Save JSON file
    json_path = os.path.join(save_dir, "time_series_analysis.json")
    with open(json_path, "w") as f:
        json.dump(json_output, f, indent=4)

    print(f"Plotly JSON saved at: {json_path}")
