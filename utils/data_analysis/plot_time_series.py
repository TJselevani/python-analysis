import os
import matplotlib.pyplot as plt
from config import FILES_DIR
from utils.data_analysis.analyze_time_series import analyze_time_series


def plot_time_series_analysis(ts_data, vehicle_id):
    """
    Plot the time series data and its components.

    Parameters:
    - ts_data: Time series data
    - vehicle_id: Vehicle ID for title
    """
    plt.figure(figsize=(14, 8))

    # Plot the original time series
    plt.subplot(2, 1, 1)
    plt.plot(ts_data.index, ts_data.values)
    plt.title(f"Daily Earnings for Vehicle {vehicle_id}")
    plt.ylabel("Amount (KSH)")
    plt.grid(True)

    # Try to plot the decomposition if we have enough data
    decomposition = analyze_time_series(ts_data)
    if decomposition:
        plt.figure(figsize=(14, 12))
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
        f1 = os.path.join(FILES_DIR, f"time_series_decomposition_{vehicle_id}.png")
        plt.savefig(f1, dpi=300)

    plt.tight_layout()
    f2 = os.path.join(FILES_DIR, f"time_series_analysis_{vehicle_id}.png")
    plt.savefig(f2, dpi=300)


def plot_prophet_time_series_analysis(data, vehicle_id):
    """
    Plot the time series data and its components.

    Parameters:
    - data: Time series data
    - vehicle_id: Vehicle ID for title
    """
    plt.figure(figsize=(14, 8))

    # Plot the original time series
    plt.subplot(2, 1, 1)
    plt.plot(data["ds"], data["y"])
    plt.title(f"Daily Earnings for Vehicle {vehicle_id}")
    plt.ylabel("Amount (KSH)")
    plt.grid(True)

    # Try to plot the decomposition if we have enough data
    decomposition = analyze_time_series(data)
    if decomposition:
        plt.figure(figsize=(14, 12))
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
        f1 = os.path.join(FILES_DIR, f"time_series_decomposition_pr_{vehicle_id}.png")
        plt.savefig(f1, dpi=300)

    plt.tight_layout()
    f2 = os.path.join(FILES_DIR, f"time_series_analysis_pr_{vehicle_id}.png")
    plt.savefig(f2, dpi=300)
