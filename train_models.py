# flake8: noqa E501
import os
import sys
import pandas as pd
import joblib

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import settings
from utils.data_preparation.prepare_time_series import (
    prepare_time_series_data,
    prepare_prophet_time_series_data,
)
from utils.data_preparation.prepare_features import prepare_features
from utils.model.ml.train import train_ml_model
from utils.model.arima.train import train_arima_model
from utils.model.sarima.train import train_sarima_model
from utils.model.prophet.train import train_prophet_model

def train_and_save_models():
    """
    Loads data, trains all models for each vehicle, and saves them to the models directory.
    """
    print("Starting model training...")
    
    # Create models directory if it doesn't exist
    os.makedirs(settings.MODELS_DIR, exist_ok=True)
    
    data = pd.read_csv(settings.DATA_CSV_FILE)
    data["created_at"] = pd.to_datetime(data["created_at"])
    
    unique_vehicles = data['vehicle_booked'].dropna().unique()

    for vehicle_id in unique_vehicles:
        print(f"--- Training models for vehicle: {vehicle_id} ---")

        # Prepare data
        ts_data = prepare_time_series_data(data, vehicle_id)
        ts_data_prophet = prepare_prophet_time_series_data(data, vehicle_id)
        features_df = prepare_features(ts_data)

        # Train and save ML model
        ml_model, _, _, _, _ = train_ml_model(features_df)
        joblib.dump(ml_model, os.path.join(settings.MODELS_DIR, f"ml_model_{vehicle_id}.joblib"))
        print(f"Saved ML model for {vehicle_id}")

        # Train and save ARIMA model
        arima_model = train_arima_model(ts_data)
        if arima_model:
            joblib.dump(arima_model, os.path.join(settings.MODELS_DIR, f"arima_model_{vehicle_id}.joblib"))
            print(f"Saved ARIMA model for {vehicle_id}")

        # Train and save SARIMA model
        sarima_model = train_sarima_model(ts_data)
        if sarima_model:
            joblib.dump(sarima_model, os.path.join(settings.MODELS_DIR, f"sarima_model_{vehicle_id}.joblib"))
            print(f"Saved SARIMA model for {vehicle_id}")
            
        # Train and save Prophet model
        prophet_model, _ = train_prophet_model(ts_data_prophet, forecast_days=30) # forecast_days is not used for saving
        if prophet_model:
            joblib.dump(prophet_model, os.path.join(settings.MODELS_DIR, f"prophet_model_{vehicle_id}.joblib"))
            print(f"Saved Prophet model for {vehicle_id}")

    print("Model training finished.")

if __name__ == "__main__":
    train_and_save_models()
