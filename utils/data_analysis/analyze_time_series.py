from statsmodels.tsa.seasonal import seasonal_decompose
import pandas as pd


def analyze_time_series(ts_data):
    """
    Analyze time series data to detect trends, seasonality, etc.

    Parameters:
    - ts_data: Time series data with datetime index

    Returns:
    - Decomposition results
    """
    # Try to decompose the time series into trend, seasonal, and residual components
    try:
        # Only decompose if we have enough data points
        if len(ts_data) >= 14:  # Need sufficient data for meaningful decomposition
            decomposition = seasonal_decompose(
                ts_data, model="additive", period=7
            )  # Weekly seasonality
            return decomposition
        else:
            print("Not enough data points for decomposition (need at least 14)")
            return None
    except Exception as e:
        print(f"Error in decomposition: {e}")
        return None


def analyze_prophet_time_series(data):
    """
    Analyze time series data to detect trends, seasonality, etc.

    Parameters:
    - data: Time series data with datetime index

    Returns:
    - Decomposition results
    """
    # Try to decompose the time series into trend, seasonal, and residual components
    try:
        # Fill any potential gaps in the data
        if isinstance(data, pd.DataFrame) and "y" in data.columns:
            ts_data = data.set_index("ds")["y"]
        else:
            ts_data = data

        # Only decompose if we have enough data points
        if len(ts_data) >= 14:  # Need sufficient data for meaningful decomposition
            decomposition = seasonal_decompose(
                ts_data, model="additive", period=7
            )  # Weekly seasonality
            return decomposition
        else:
            print("Not enough data points for decomposition (need at least 14)")
            return None
    except Exception as e:
        print(f"Error in decomposition: {e}")
        return None
