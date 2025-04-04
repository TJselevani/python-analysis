import os
from config import FILES_DIR
import matplotlib.pyplot as plt


def plot_ensemble_forecast(historical_data, ensemble_df, vehicle_id):
    """
    Plot the ensemble forecast.

    Parameters:
    - historical_data: Historical time series data
    - ensemble_df: DataFrame with ensemble forecast
    - vehicle_id: Vehicle ID for title
    """
    plt.figure(figsize=(14, 8))

    # Plot historical data
    plt.plot(historical_data.index, historical_data.values, label="Historical Data")

    # Plot individual forecasts
    forecast_columns = [col for col in ensemble_df.columns if "forecast" in col]
    for col in forecast_columns:
        if col != "ensemble_forecast":
            plt.plot(
                ensemble_df["date"],
                ensemble_df[col],
                label=col.replace("_forecast", ""),
                alpha=0.5,
            )

    # Plot ensemble forecast
    plt.plot(
        ensemble_df["date"],
        ensemble_df["ensemble_forecast"],
        label="Ensemble Forecast",
        color="red",
        linewidth=2,
    )

    plt.title(f"Ensemble Forecast for Vehicle {vehicle_id}")
    plt.xlabel("Date")
    plt.ylabel("Earnings (KSH)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    f1 = os.path.join(FILES_DIR, f"{vehicle_id}/forecast/ensemble_forecast.png")
    plt.savefig(f1, dpi=300)
    plt.show()
