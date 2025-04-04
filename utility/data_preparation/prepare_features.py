import numpy as np


def prepare_features(ts_data):
    """
    Prepare features for machine learning models.
    """
    df = ts_data.reset_index()
    df.columns = ["date", "earnings"]

    # Ensure earnings column is float upfront
    df["earnings"] = df["earnings"].astype(float)  # <-- Fix here

    # Date features
    dates = df["date"].dt
    df["dayofweek"] = dates.dayofweek.astype(np.int8)
    df["month"] = dates.month.astype(np.int8)
    df["day"] = dates.day.astype(np.int8)
    df["dayofyear"] = dates.dayofyear.astype(np.int16)
    df["week"] = dates.isocalendar().week.astype(np.int8)  # <-- Fix here
    df["is_weekend"] = (df["dayofweek"] >= 5).astype(np.int8)

    # Lag features with explicit dtype
    for lag in range(1, 8):
        df[f"lag_{lag}"] = df["earnings"].shift(lag).astype(np.float32)

    # Rolling features
    rolling = df["earnings"].rolling(window=3)
    df["rolling_mean_3"] = rolling.mean().astype(np.float32)
    df["rolling_mean_7"] = df["earnings"].rolling(window=7).mean().astype(np.float32)
    df["rolling_std_7"] = df["earnings"].rolling(window=7).std().astype(np.float32)

    return df.dropna()


# def prepare_features(ts_data):
#     """
#     Prepare features for machine learning models.

#     Parameters:
#     - ts_data: Time series data

#     Returns:
#     - DataFrame with features
#     """
#     df = ts_data.reset_index()
#     df.columns = ["date", "earnings"]

#     # Extract date features
#     df["dayofweek"] = df["date"].dt.dayofweek
#     df["month"] = df["date"].dt.month
#     df["day"] = df["date"].dt.day
#     df["dayofyear"] = df["date"].dt.dayofyear
#     df["week"] = df["date"].dt.isocalendar().week
#     df["is_weekend"] = df["dayofweek"].apply(lambda x: 1 if x >= 5 else 0)

#     # Create lag features
#     for lag in range(1, 8):  # Create lags up to 7 days
#         df[f"lag_{lag}"] = df["earnings"].shift(lag)

#     # Create rolling window features
#     df["rolling_mean_3"] = df["earnings"].rolling(window=3).mean()
#     df["rolling_mean_7"] = df["earnings"].rolling(window=7).mean()
#     df["rolling_std_7"] = df["earnings"].rolling(window=7).std()

#     # Drop rows with NaN values (due to lag/rolling features)
#     df = df.dropna()

#     return df
