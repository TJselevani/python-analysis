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
        save_dir = f"{vehicle_id}/analysis/time_series_decomposition.png"
        f1 = os.path.join(FILES_DIR, save_dir)
        plt.savefig(f1, dpi=300)

    plt.tight_layout()
    save_dir = f"{vehicle_id}/analysis/time_series_analysis.png"
    f2 = os.path.join(FILES_DIR, save_dir)
    plt.savefig(f2, dpi=300)
