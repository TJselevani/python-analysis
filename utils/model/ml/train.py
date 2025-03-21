from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor


def train_ml_model(features_df, forecast_days=30):
    """
    Train a machine learning model for forecasting.

    Parameters:
    - features_df: DataFrame with features
    - forecast_days: Number of days to forecast

    Returns:
    - model: Trained model
    - X_train, X_test, y_train, y_test: Train/test split data
    """
    # Define features and target
    X = features_df.drop(["date", "earnings"], axis=1)
    y = features_df["earnings"]

    # Split data for training and testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, shuffle=False
    )

    # Train a Random Forest model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    return model, X_train, X_test, y_train, y_test
