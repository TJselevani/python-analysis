import matplotlib.pyplot as plt
import pandas as pd
import os
from config import FILES_DIR


def plot_forecast(historical_data, forecast_df, vehicle_id, model_type):
    """
    Plot the historical data and forecast.

    Parameters:
    - historical_data: Historical time series data
    - forecast_df: DataFrame with forecasted values
    - vehicle_id: Vehicle ID for title
    - model_type: Type of model used (ML, ARIMA, etc.)
    """
    plt.figure(figsize=(14, 8))

    # Plot historical data
    plt.plot(historical_data.index, historical_data.values, label="Historical Data")

    # Plot forecast
    if isinstance(forecast_df, pd.DataFrame) and "date" in forecast_df.columns:
        plt.plot(
            forecast_df["date"], forecast_df["earnings"], label="Forecast", color="red"
        )

    plt.title(f"{model_type} Forecast for Vehicle {vehicle_id}")
    plt.xlabel("Date")
    plt.ylabel("Earnings (KSH)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    f2 = os.path.join(FILES_DIR, f"{model_type.lower()}_forecast_{vehicle_id}.png")
    plt.savefig(f2, dpi=300)
    plt.show()
