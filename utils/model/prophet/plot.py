import matplotlib.pyplot as plt
import os
from config import FILES_DIR


def plot_prophet_forecast(model, forecast, vehicle_id):
    """
    Plot the Prophet forecast.

    Parameters:
    - model: Trained Prophet model
    - forecast: Forecast DataFrame from Prophet
    - vehicle_id: Vehicle ID for the title
    """
    # Plot the forecast
    fig1 = model.plot(forecast)
    plt.title(f"Earnings Forecast for Vehicle {vehicle_id}")
    plt.xlabel("Date")
    plt.ylabel("Amount (KSH)")
    f1 = os.path.join(FILES_DIR, f"prophet_earnings_forecast_{vehicle_id}.png")
    plt.savefig(f1, dpi=300)

    # Plot the components of the forecast
    fig2 = model.plot_components(forecast)
    f1 = os.path.join(FILES_DIR, f"forecast_components_{vehicle_id}.png")
    plt.savefig(f1, dpi=300)
