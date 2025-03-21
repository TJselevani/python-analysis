import pandas as pd


def prepare_time_series_data(data, vehicle_id=None, resample_freq="D"):
    """
    Prepare data for time series analysis by resampling and aggregating by date.

    Parameters:
    - data: DataFrame containing the transaction data
    - vehicle_id: Optional vehicle ID to filter by
    - resample_freq: Frequency to resample the data ('D' for daily, 'H' for hourly, etc.)

    Returns:
    - Resampled DataFrame with date as index and aggregate earnings
    """
    # Convert created_at to datetime if not already
    data["created_at"] = pd.to_datetime(data["created_at"])

    # Filter for the specified vehicle if provided
    if vehicle_id:
        df = data[data["vehicle_booked"] == vehicle_id].copy()
    else:
        df = data.copy()

    # Filter for credit transactions only (passenger payments)
    credit_data = df[df["transaction_type"] == "CREDIT"].copy()

    # Set the datetime as index
    credit_data.set_index("created_at", inplace=True)

    # Resample and sum the amounts for each period
    earnings = credit_data.resample(resample_freq)["amount"].sum().fillna(0)

    return earnings


def prepare_prophet_time_series_data(data, vehicle_id=None, resample_freq="D"):
    """
    Prepare data for time series analysis by resampling and aggregating by date.

    Parameters:
    - data: DataFrame containing the transaction data
    - vehicle_id: Optional vehicle ID to filter by
    - resample_freq: Frequency to resample the data ('D' for daily, 'H' for hourly, etc.)

    Returns:
    - Resampled DataFrame with date as index and aggregate earnings
    """
    # Convert created_at to datetime if not already
    data["created_at"] = pd.to_datetime(data["created_at"])

    # Filter for the specified vehicle if provided
    if vehicle_id:
        df = data[data["vehicle_booked"] == vehicle_id].copy()
    else:
        df = data.copy()

    # Filter for credit transactions only (passenger payments)
    credit_data = df[df["transaction_type"] == "CREDIT"].copy()

    # Set the datetime as index
    credit_data.set_index("created_at", inplace=True)

    # Resample and sum the amounts for each period
    earnings = credit_data.resample(resample_freq)["amount"].sum().fillna(0)

    # Convert to DataFrame for easier manipulation
    earnings_df = earnings.reset_index()
    earnings_df.columns = ["ds", "y"]  # Prophet requires these column names

    return earnings_df
