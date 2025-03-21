from statsmodels.tsa.arima.model import ARIMA


def train_arima_model(ts_data):
    """
    Train an ARIMA model for time series forecasting.

    Parameters:
    - ts_data: Time series data

    Returns:
    - model: Trained ARIMA model
    """
    # Simple ARIMA model with default parameters
    try:
        model = ARIMA(ts_data, order=(5, 1, 0))
        model_fit = model.fit()
        return model_fit
    except Exception as e:
        print(f"Error training ARIMA model: {e}")
        try:
            # Try a simpler model if the first one fails
            model = ARIMA(ts_data, order=(1, 1, 0))
            model_fit = model.fit()
            return model_fit
        except Exception as e:
            print(f"Error training simpler ARIMA model: {e}")
            return None
