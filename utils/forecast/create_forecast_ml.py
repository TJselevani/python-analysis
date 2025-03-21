import pandas as pd
import numpy as np


def forecast_future_ml(model, features_df, forecast_days=30):
    """
    Forecast future values using the trained ML model.

    Parameters:
    - model: Trained model
    - features_df: DataFrame with features
    - forecast_days: Number of days to forecast

    Returns:
    - DataFrame with forecasted values
    """
    # Get the last date in the data
    last_date = features_df["date"].max()

    # Create a DataFrame for future dates
    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(days=1), periods=forecast_days
    )
    future_df = pd.DataFrame({"date": future_dates})

    # Extract date features for future dates
    future_df["dayofweek"] = future_df["date"].dt.dayofweek
    future_df["month"] = future_df["date"].dt.month
    future_df["day"] = future_df["date"].dt.day
    future_df["dayofyear"] = future_df["date"].dt.dayofyear
    future_df["week"] = future_df["date"].dt.isocalendar().week
    future_df["is_weekend"] = future_df["dayofweek"].apply(lambda x: 1 if x >= 5 else 0)

    # Initialize prediction column
    future_df["earnings"] = 0

    # Iterate through future dates and predict
    for i in range(forecast_days):
        if i < 7:
            # For the first 7 days, use the last known values for lag features
            lag_data = features_df["earnings"].iloc[-7:].values
            for lag in range(1, 8):
                if lag <= i:
                    # Use previously predicted values
                    future_df.loc[i, f"lag_{lag}"] = future_df["earnings"].iloc[i - lag]
                else:
                    # Use historical values
                    future_df.loc[i, f"lag_{lag}"] = lag_data[-(lag - i)]
        else:
            # After 7 days, use only predicted values for lag features
            for lag in range(1, 8):
                future_df.loc[i, f"lag_{lag}"] = future_df["earnings"].iloc[i - lag]

        # Calculate rolling features
        if i < 3:
            # For the first 3 days, use a mix of historical and predicted data
            values = list(features_df["earnings"].iloc[-3 + i :].values) + list(
                future_df["earnings"].iloc[:i].values
            )
            future_df.loc[i, "rolling_mean_3"] = np.mean(values)
        else:
            # After 3 days, use only predicted values
            future_df.loc[i, "rolling_mean_3"] = (
                future_df["earnings"].iloc[i - 3 : i].mean()
            )

        if i < 7:
            # For the first 7 days, use a mix of historical and predicted data
            values = list(features_df["earnings"].iloc[-7 + i :].values) + list(
                future_df["earnings"].iloc[:i].values
            )
            future_df.loc[i, "rolling_mean_7"] = np.mean(values)
            future_df.loc[i, "rolling_std_7"] = np.std(values) if len(values) > 1 else 0
        else:
            # After 7 days, use only predicted values
            future_df.loc[i, "rolling_mean_7"] = (
                future_df["earnings"].iloc[i - 7 : i].mean()
            )
            future_df.loc[i, "rolling_std_7"] = (
                future_df["earnings"].iloc[i - 7 : i].std()
            )

        # Make prediction for this day
        X_future = future_df.iloc[i : i + 1].drop(["date", "earnings"], axis=1)
        future_df.loc[i, "earnings"] = model.predict(X_future)[0]

    return future_df
