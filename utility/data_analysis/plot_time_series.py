import os
import json
import plotly.graph_objects as go
from config import JSON_DIR
from utility.data_analysis.analyze_time_series import analyze_time_series


def plot_time_series_analysis(ts_data, vehicle_id):
    """
    Generate Plotly time series analysis and save it as JSON.

    Parameters:
    - ts_data: Time series data
    - vehicle_id: Vehicle ID for title
    """
    # Define JSON directory paths
    json_save_dir = os.path.join(JSON_DIR, vehicle_id, "analysis")
    dec_save_dir = os.path.join(JSON_DIR, vehicle_id, "decomposition")
    os.makedirs(json_save_dir, exist_ok=True)
    os.makedirs(dec_save_dir, exist_ok=True)

    # Create main figure for original time series
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

    # fig_main.show()

    # Initialize JSON output
    json_output = {"time_series_analysis": json.loads(fig_main.to_json())}

    # Time series decomposition
    decomposition = analyze_time_series(ts_data)
    if decomposition:
        fig_decomposition = go.Figure()

        # COMBINED decomposition
        fig_decomposition.add_trace(
            go.Scatter(
                x=ts_data.index, y=decomposition.observed, mode="lines", name="Observed"
            )
        )
        fig_decomposition.add_trace(
            go.Scatter(
                x=ts_data.index, y=decomposition.trend, mode="lines", name="Trend"
            )
        )
        fig_decomposition.add_trace(
            go.Scatter(
                x=ts_data.index,
                y=decomposition.seasonal,
                mode="lines",
                name="Seasonality",
            )
        )
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

        # fig_decomposition.show()
        decomposition_output = {
            "decomposition": json.loads(fig_decomposition.to_json())
        }
        path = os.path.join(json_save_dir, "time_series_decomposition.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(decomposition_output, f, indent=4)
        print(f"Analysis Decomposition JSON saved at: {path}")

        # OBSERVED
        fig_observed = go.Figure()

        fig_observed.add_trace(
            go.Scatter(
                x=ts_data.index, y=decomposition.observed, mode="lines", name="Observed"
            )
        )

        fig_observed.update_layout(
            title="Time Series Decomposition (Observed)",
            xaxis_title="Date",
            yaxis_title="Value",
            template="plotly_dark",
        )

        observed_output = {"decomposition_observed": json.loads(fig_observed.to_json())}
        path = os.path.join(dec_save_dir, "observed.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(observed_output, f, indent=4)
        print(f"Observed Decomposition JSON saved at: {path}")

        # TREND
        fig_trend = go.Figure()

        fig_trend.add_trace(
            go.Scatter(
                x=ts_data.index, y=decomposition.trend, mode="lines", name="Trend"
            )
        )

        fig_trend.update_layout(
            title="Time Series Decomposition (Trend)",
            xaxis_title="Date",
            yaxis_title="Value",
            template="plotly_dark",
        )

        trend_output = {"decomposition_trend": json.loads(fig_trend.to_json())}
        path = os.path.join(dec_save_dir, "trend.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(trend_output, f, indent=4)
        print(f"Trend Decomposition JSON saved at: {path}")

        # RESIDUALS
        fig_residual = go.Figure()

        fig_residual.add_trace(
            go.Scatter(
                x=ts_data.index, y=decomposition.resid, mode="lines", name="Residuals"
            )
        )

        fig_residual.update_layout(
            title="Time Series Decomposition (Residuals)",
            xaxis_title="Date",
            yaxis_title="Value",
            template="plotly_dark",
        )

        residual_output = {
            "decomposition_residuals": json.loads(fig_residual.to_json())
        }
        path = os.path.join(dec_save_dir, "residuals.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(residual_output, f, indent=4)
        print(f"Residuals Decomposition JSON saved at: {path}")

        # SEASONALITY
        fig_seasonal = go.Figure()

        fig_seasonal.add_trace(
            go.Scatter(
                x=ts_data.index,
                y=decomposition.seasonal,
                mode="lines",
                name="Seasonality",
            )
        )

        fig_seasonal.update_layout(
            title="Time Series Decomposition (Residuals)",
            xaxis_title="Date",
            yaxis_title="Value",
            template="plotly_dark",
        )

        seasonal_output = {
            "decomposition_seasonality": json.loads(fig_seasonal.to_json())
        }
        path = os.path.join(dec_save_dir, "seasonality.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(seasonal_output, f, indent=4)
        print(f"Seasonality Decomposition JSON saved at: {path}")

    # Save as JSON
    json_path = os.path.join(json_save_dir, "time_series_analysis.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_output, f, indent=4)

    print(f"Time Series Analysis JSON saved at: {json_path}")
