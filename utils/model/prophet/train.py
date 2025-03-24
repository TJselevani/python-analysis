from prophet import Prophet


def train_prophet_model(data, forecast_days=30):
    """
    Train a Prophet model for forecasting.

    Parameters:
    - data: DataFrame with 'ds' (dates) and 'y' (target values) columns
    - forecast_days: Number of days to forecast into the future

    Returns:
    - model: Trained Prophet model
    - forecast: Forecast DataFrame
    """
    # Initialize and train the model
    prophet_model = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=True,
        seasonality_mode="multiplicative",
        interval_width=0.95,  # 95% confidence interval
    )

    # Add custom seasonality for weekday vs weekend
    prophet_model.add_seasonality(name="weekday_weekend", period=7, fourier_order=3)

    # Fit the model
    prophet_model.fit(data)

    # Create a dataframe for future predictions
    future = prophet_model.make_future_dataframe(periods=forecast_days)

    # Make predictions
    prophet_forecast = prophet_model.predict(future)

    return prophet_model, prophet_forecast
