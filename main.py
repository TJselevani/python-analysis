import pandas as pd
from utils.data_preparation.prepare_time_series import prepare_time_series_data

from utils.ensemble.ensemble_forecast import ensemble_forecast
from utils.ensemble.plot_ensemble_forecast import plot_ensemble_forecast

from utils.prediction.vehicle_prediction import run_prediction_for_vehicle


# Example usage
if __name__ == "__main__":
    # Path to your data
    data_path = "/home/tjselevani/Desktop/Apps/vscode/python/python analysis/data/last-3-months-transactions.csv"

    # Vehicle to analyze
    vehicle_id = "SM055"

    # Run prediction for the vehicle
    forecasts = run_prediction_for_vehicle(data_path, vehicle_id, forecast_days=30)

    # Create ensemble forecast
    ensemble_df = ensemble_forecast(forecasts)

    # Plot ensemble forecast
    ts_data = prepare_time_series_data(pd.read_csv(data_path), vehicle_id)
    plot_ensemble_forecast(ts_data, ensemble_df, vehicle_id)

    # Display the forecast for the next 7 days
    print("Ensemble Forecast for the next 7 days:")
    print(ensemble_df[["date", "ensemble_forecast"]].head(7))

    # Calculate aggregate statistics
    total_predicted = ensemble_df["ensemble_forecast"].head(7).sum()
    average_daily = ensemble_df["ensemble_forecast"].head(7).mean()
    print(f"Total predicted earnings for next 7 days: {total_predicted:.2f} KSH")
    print(f"Average daily earnings: {average_daily:.2f} KSH")
