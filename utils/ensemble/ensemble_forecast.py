def ensemble_forecast(forecasts):
    """
    Create an ensemble forecast by averaging predictions from different models.

    Parameters:
    - forecasts: Dictionary with forecasts from different models

    Returns:
    - DataFrame with ensemble forecast
    """
    # Initialize with the first forecast
    ensemble_df = forecasts["ml"][["date", "earnings"]].copy()
    ensemble_df.rename(columns={"earnings": "ml_forecast"}, inplace=True)

    # Add other forecasts if available
    if forecasts["arima"] is not None:
        arima_df = forecasts["arima"][["date", "earnings"]].copy()
        ensemble_df = ensemble_df.merge(
            arima_df, on="date", how="left", suffixes=("", "_arima")
        )
        ensemble_df.rename(columns={"earnings": "arima_forecast"}, inplace=True)

    if forecasts["sarima"] is not None:
        sarima_df = forecasts["sarima"][["date", "earnings"]].copy()
        ensemble_df = ensemble_df.merge(
            sarima_df, on="date", how="left", suffixes=("", "_sarima")
        )
        ensemble_df.rename(columns={"earnings": "sarima_forecast"}, inplace=True)

    if forecasts["prophet"] is None:
        prophet_df = forecasts["prophet"][["date", "earnings"]].copy()
        ensemble_df = ensemble_df.merge(
            prophet_df, on="date", how="left", suffixes=("", "_prophet")
        )
        ensemble_df.rename(columns={"earnings": "prophet_forecast"}, inplace=True)

    # Calculate ensemble forecast (average of available forecasts)
    forecast_columns = [col for col in ensemble_df.columns if "forecast" in col]
    ensemble_df["ensemble_forecast"] = ensemble_df[forecast_columns].mean(axis=1)

    return ensemble_df
