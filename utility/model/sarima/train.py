from statsmodels.tsa.statespace.sarimax import SARIMAX


def train_sarima_model(ts_data):
    """
    Train a SARIMA model for time series forecasting.

    Parameters:
    - ts_data: Time series data

    Returns:
    - model: Trained SARIMA model
    """
    try:
        # SARIMA model with seasonal component (weekly)
        model = SARIMAX(ts_data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 7))
        model_fit = model.fit(disp=False)
        return model_fit
    except Exception as e:
        print(f"Error training SARIMA model: {e}")
        try:
            # Try a simpler model if the first one fails
            model = SARIMAX(ts_data, order=(1, 1, 0), seasonal_order=(1, 0, 0, 7))
            model_fit = model.fit(disp=False)
            return model_fit
        except Exception as e:
            print(f"Error training simpler SARIMA model: {e}")
            return None
