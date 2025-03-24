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
    plt.figure(figsize=(16, 12))

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
    save_dir = f"{vehicle_id}/forecast/{model_type.lower()}_forecast.png"
    f1 = os.path.join(FILES_DIR, save_dir)
    plt.savefig(f1, dpi=300)
    plt.show()


def plot_prophet_forecast(historical_data, model, forecast, vehicle_id, model_type):
    """
    Plot the Prophet forecast.

    Parameters:
    - model: Trained Prophet model
    - forecast: Forecast DataFrame from Prophet
    - vehicle_id: Vehicle ID for the title
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
    f1 = os.path.join(
        FILES_DIR, f"{vehicle_id}/forecast/{model_type.lower()}_forecast.png"
    )
    plt.savefig(f1, dpi=300)
    plt.show()

    # Plot the components of the forecast
    model.plot_components(forecast)
    plt.title(f"{model_type} Forecast Components for Vehicle {vehicle_id}")
    plt.xlabel("Date")
    plt.ylabel("Earnings (KSH)")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    save_dir = f"{vehicle_id}/analysis/time_series_components.png"
    f1 = os.path.join(FILES_DIR, save_dir)
    plt.savefig(f1, dpi=300)
    plt.show()
