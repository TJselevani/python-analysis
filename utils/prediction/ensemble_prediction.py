import pandas as pd
from utils.data_preparation.prepare_time_series import (
    prepare_time_series_data,
    prepare_prophet_time_series_data,
)
from utils.data_preparation.prepare_features import prepare_features

from utils.data_analysis.plot_time_series import plot_time_series_analysis

from utils.model.ml.train import train_ml_model
from utils.model.evaluate_model import evaluate_model
from utils.model.arima.train import train_arima_model
from utils.model.sarima.train import train_sarima_model
from utils.model.prophet.train import train_prophet_model

from utils.forecast.create_forecast_ml import forecast_future_ml
from utils.forecast.create_forecast_arima import forecast_future_arima
from utils.forecast.plot_forecast import plot_forecast, plot_prophet_forecast


def run_prediction_for_vehicle(data_path, vehicle_id, forecast_days=30):
    """
    Run the complete prediction pipeline for a specific vehicle.

    Parameters:
    - data_path: Path to the CSV file with transaction data
    - vehicle_id: ID of the vehicle to analyze
    - forecast_days: Number of days to forecast

    Returns:
    - Dictionary with forecasts from different models
    """
    # Import the data
    data = pd.read_csv(data_path)

    # Convert 'created_at' column to datetime
    data["created_at"] = pd.to_datetime(data["created_at"])

    # Prepare time series data
    ts_data = prepare_time_series_data(data, vehicle_id)

    # Analyze and plot time series
    plot_time_series_analysis(ts_data, vehicle_id)

    """ 
    Linear Regression ML Model 
    """

    # Prepare features for ML model
    features_df = prepare_features(ts_data)

    # Train ML model
    ml_model, X_train, X_test, y_train, y_test = train_ml_model(features_df)

    # Evaluate ML model
    ml_metrics = evaluate_model(ml_model, X_test, y_test)
    print(f"ML Model Metrics: {ml_metrics}")

    # Forecast with ML model
    ml_forecast = forecast_future_ml(ml_model, features_df, forecast_days)

    # Plot ML forecast
    plot_forecast(ts_data, ml_forecast, vehicle_id, "ML")

    """
    Arima ML Model
    """

    # Train ARIMA model
    arima_model = train_arima_model(ts_data)

    # Forecast with ARIMA model
    if arima_model:
        arima_forecast = forecast_future_arima(arima_model, ts_data, forecast_days)

        # Plot ARIMA forecast
        if arima_forecast is not None:
            plot_forecast(ts_data, arima_forecast, vehicle_id, "ARIMA")
    else:
        arima_forecast = None

    """
    Sarimax Ml Model
    """

    # Train SARIMA model
    sarima_model = train_sarima_model(ts_data)

    # Forecast with SARIMA model
    if sarima_model:
        sarima_forecast = forecast_future_arima(sarima_model, ts_data, forecast_days)

        # Plot SARIMA forecast
        if sarima_forecast is not None:
            plot_forecast(ts_data, sarima_forecast, vehicle_id, "SARIMA")
    else:
        sarima_forecast = None

    """
    Prophet ML Model
    """

    # Prepare time series data
    ts_data = prepare_prophet_time_series_data(data, vehicle_id)

    # Train the model and get forecast
    prophet_model, prophet_forecast = train_prophet_model(ts_data, forecast_days)

    # Evaluate Prophet model
    # ml_metrics = evaluate_prophet_accuracy(ts_data, prophet_forecast)
    # print(f"PROPHET Model Metrics: {ml_metrics}")

    if prophet_model:
        plot_prophet_forecast(
            ts_data, prophet_model, prophet_forecast, vehicle_id, "PROPHET"
        )
    else:
        prophet_model = None

    print(f"Forecast completed for vehicle {vehicle_id}")
    print(f"Forecasted for {forecast_days} days into the future")

    # Return forecasts from different models
    return {
        "ml": ml_forecast,
        "arima": arima_forecast,
        "sarima": sarima_forecast,
        "prophet": prophet_forecast,
    }
