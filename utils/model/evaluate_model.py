from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np


def evaluate_model(model, X_test, y_test):
    """
    Evaluate the model performance.

    Parameters:
    - model: Trained model
    - X_test: Test features
    - y_test: Test target

    Returns:
    - Dictionary with evaluation metrics
    """
    y_pred = model.predict(X_test)

    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    return {"MAE": mae, "RMSE": rmse, "R2": r2}


def evaluate_prophet_accuracy(actual, predicted):
    """
    Evaluate the forecast accuracy.

    Parameters:
    - actual: Actual values
    - predicted: Predicted values

    Returns:
    - Dictionary with evaluation metrics
    """
    mae = mean_absolute_error(actual, predicted)
    rmse = np.sqrt(mean_squared_error(actual, predicted))
    r2 = r2_score(actual, predicted)

    return {"MAE": mae, "RMSE": rmse, "R2": r2}
