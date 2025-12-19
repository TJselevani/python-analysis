import pandas as pd
import joblib
import os
import sys
from fastapi import HTTPException  # Import HTTPException

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import settings
from utils.data_preparation.prepare_time_series import (
    prepare_time_series_data,
    prepare_prophet_time_series_data,
)
from utils.data_preparation.prepare_features import prepare_features
from utils.ensemble.ensemble_forecast import ensemble_forecast
from utils.forecast.create_forecast_ml import forecast_future_ml
from utils.forecast.create_forecast_arima import (
    forecast_future_arima,
)  # Used for SARIMA too
from prophet import Prophet


def load_models_for_vehicle(vehicle_id):
    """Loads pre-trained models for a given vehicle ID."""
    models = {}
    try:
        models["ml"] = joblib.load(
            os.path.join(settings.MODELS_DIR, f"ml_model_{vehicle_id}.joblib")
        )
        models["arima"] = joblib.load(
            os.path.join(settings.MODELS_DIR, f"arima_model_{vehicle_id}.joblib")
        )
        models["sarima"] = joblib.load(
            os.path.join(settings.MODELS_DIR, f"sarima_model_{vehicle_id}.joblib")
        )
        models["prophet"] = joblib.load(
            os.path.join(settings.MODELS_DIR, f"prophet_model_{vehicle_id}.joblib")
        )
    except FileNotFoundError as e:
        print(f"Error loading models for {vehicle_id}: {e}")
        raise FileNotFoundError(
            f"Missing model files for vehicle {vehicle_id}. Please ensure models are trained."
        ) from e
    return models


def run_prediction(vehicle_id: str, forecast_days: int = 30):
    """
    Loads pre-trained models, generates forecasts, creates an ensemble, and returns it.
    """
    # Load raw data and prepare time series
    data = pd.read_csv(settings.DATA_CSV_FILE)
    data["created_at"] = pd.to_datetime(data["created_at"])
    ts_data = prepare_time_series_data(data, vehicle_id)

    # Check if ts_data is empty after preparation
    if ts_data.empty:
        raise HTTPException(
            status_code=404,
            detail=f"No historical data available for vehicle {vehicle_id} to make a forecast.",
        )

    # Load models
    models = load_models_for_vehicle(vehicle_id)

    forecasts = {}

    # ML Forecast
    features_df = prepare_features(ts_data)
    ml_forecast = forecast_future_ml(models["ml"], features_df, forecast_days)
    forecasts["ml"] = ml_forecast

    # ARIMA Forecast
    arima_forecast = forecast_future_arima(models["arima"], ts_data, forecast_days)
    forecasts["arima"] = arima_forecast

    # SARIMA Forecast
    sarima_forecast = forecast_future_arima(models["sarima"], ts_data, forecast_days)
    forecasts["sarima"] = sarima_forecast

    # Prophet Forecast
    # Prophet requires specific data preparation for forecasting
    ts_data_prophet = prepare_prophet_time_series_data(data, vehicle_id)
    future_prophet = models["prophet"].make_future_dataframe(
        periods=forecast_days, include_history=False
    )
    prophet_forecast_df = models["prophet"].predict(future_prophet)

    prophet_forecast = prophet_forecast_df[["ds", "yhat"]].rename(
        columns={"ds": "date", "yhat": "forecast"}
    )
    prophet_forecast["date"] = pd.to_datetime(
        prophet_forecast["date"]
    ).dt.date  # Ensure date format consistency
    forecasts["prophet"] = prophet_forecast

    # Create ensemble forecast
    ensemble_df = ensemble_forecast(forecasts)

    # Convert dates to string for JSON serialization
    ensemble_df["date"] = ensemble_df["date"].astype(str)

    return ensemble_df.to_dict(orient="records")


if __name__ == "__main__":
    # Example usage for testing
    try:
        sample_forecast = run_prediction(vehicle_id="SM191", forecast_days=7)
        print(json.dumps(sample_forecast, indent=2))
    except FileNotFoundError as e:
        print(f"Error: {e}. Please run `python train_models.py` first.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
