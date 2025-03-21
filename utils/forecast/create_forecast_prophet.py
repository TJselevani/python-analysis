from utils.data_preparation.prepare_time_series import prepare_prophet_time_series_data
from utils.data_analysis.plot_time_series import plot_prophet_time_series_analysis
from utils.model.prophet.train import train_prophet_model
from utils.model.prophet.plot import plot_prophet_forecast


def predict_vehicle_earnings(data, vehicle_id, resample_freq="D", forecast_days=30):
    """
    End-to-end function to predict earnings for a specific vehicle.

    Parameters:
    - data: DataFrame with transaction data
    - vehicle_id: ID of the vehicle to analyze
    - resample_freq: Frequency to resample data ('D' for daily, 'H' for hourly)
    - forecast_days: Number of days to forecast into the future

    Returns:
    - forecast: DataFrame with the forecasted values
    """
    # Prepare the data
    earnings_df = prepare_prophet_time_series_data(data, vehicle_id, resample_freq)

    # Analyze the time series
    plot_prophet_time_series_analysis(earnings_df, vehicle_id)

    # Train the model and get forecast
    model, forecast = train_prophet_model(earnings_df, forecast_days)

    # Plot the forecast
    plot_prophet_forecast(model, forecast, vehicle_id)

    # Return the forecast
    return forecast
