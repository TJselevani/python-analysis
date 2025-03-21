import pandas as pd
from utils.forecast.create_forecast_prophet import predict_vehicle_earnings


def run_prediction_for_vehicle(data_path, vehicle_id, forecast_days=30):
    """
    Run the complete prediction pipeline for a specific vehicle.

    Parameters:
    - data_path: Path to the CSV file with transaction data
    - vehicle_id: ID of the vehicle to analyze
    - forecast_days: Number of days to forecast

    Returns:
    - Forecast DataFrame
    """
    # Import the data
    data = pd.read_csv(data_path)

    # Convert 'created_at' column to datetime
    data["created_at"] = pd.to_datetime(data["created_at"])

    # Run the prediction
    forecast = predict_vehicle_earnings(data, vehicle_id, forecast_days=forecast_days)

    # Evaluate on historical data (if we split the data)
    # For this we would need to implement a train-test split

    print(f"Forecast completed for vehicle {vehicle_id}")
    print(f"Forecasted for {forecast_days} days into the future")

    # Return the forecast results
    return forecast
