import pandas as pd


def forecast_future_arima(model, ts_data, forecast_days=30):
    """
    Forecast future values using the trained ARIMA model.

    Parameters:
    - model: Trained ARIMA model
    - ts_data: Time series data
    - forecast_days: Number of days to forecast

    Returns:
    - DataFrame with forecasted values
    """
    try:
        # Get forecast
        forecast = model.forecast(steps=forecast_days)

        # Create date range for future dates
        last_date = ts_data.index[-1]
        future_dates = pd.date_range(
            start=last_date + pd.Timedelta(days=1), periods=forecast_days
        )

        # Create DataFrame with forecasted values
        forecast_df = pd.DataFrame({"date": future_dates, "earnings": forecast})

        return forecast_df
    except Exception as e:
        print(f"Error forecasting with ARIMA: {e}")
        return None
