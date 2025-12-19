import sys
import os
# Ensure the project root is in sys.path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from api.main import app # Assuming api.main is the entry point for your FastAPI app
import shutil
import json
from datetime import datetime, timedelta

# Create a TestClient
client = TestClient(app)

# Define paths for test data and models
TEST_DATA_CSV = "data/last-3-months-transactions.csv" # Using existing data for now
TEST_MODELS_DIR = "test_models"
TEST_JSON_DIR = "test_json"

@pytest.fixture(scope="module", autouse=True)
def setup_and_teardown_test_environment():
    """
    Sets up a clean environment for tests by ensuring pre-computed data and models exist.
    This fixture will:
    1. Create temporary directories for models and JSON output if they don't exist.
    2. Run the `precompute_eda.py` script to generate necessary EDA JSONs.
    3. Run the `train_models.py` script to generate necessary ML models.
    4. Clean up these directories after all tests are done.
    """
    # Override config paths for testing if necessary, or ensure scripts use base paths
    # For now, assume config paths point to project root which is fine for test_models/test_json
    
    # Ensure test directories exist
    os.makedirs(TEST_MODELS_DIR, exist_ok=True)
    os.makedirs(TEST_JSON_DIR, exist_ok=True)

    # Backup original config.py values and set test-specific values
    # This is a bit tricky without modifying config.py directly for tests.
    # For simplicity, we'll rely on the scripts to use their default paths
    # or ensure they can be overridden via environment variables if implemented later.

    print("\nSetting up test environment: Running precompute_eda.py and train_models.py...")
    # Run precompute_eda.py
    os.system("python precompute_eda.py")
    # Run train_models.py
    os.system("python train_models.py")
    print("Test environment setup complete.")

    yield # Run the tests

    print("Tearing down test environment: Removing test models and JSONs...")
    # Clean up
    if os.path.exists(TEST_MODELS_DIR):
        shutil.rmtree(TEST_MODELS_DIR)
    if os.path.exists(TEST_JSON_DIR):
        shutil.rmtree(TEST_JSON_DIR)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI application!"}

def test_get_scatter_eda_all_vehicles_success():
    # Assuming there is data for 2024-12-06 for all vehicles
    date = "2024-12-06" 
    response = client.get(f"/api/v1/eda/day/sc_bundle?date={date}")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "series" in data
    assert len(data["series"]) > 0

def test_get_scatter_eda_specific_vehicle_success():
    # Assuming there is data for 2024-12-06 for SM191
    date = "2024-12-06"
    vehicle_id = "SM191"
    response = client.get(f"/api/v1/eda/day/sc_bundle?date={date}&vehicle_id={vehicle_id}")
    assert response.status_code == 200
    data = response.json()
    assert "title" in data
    assert "series" in data
    assert len(data["series"]) > 0
    assert vehicle_id in data["title"] # Title should reflect the vehicle_id

def test_get_scatter_eda_invalid_date_format():
    date = "2024/12/06" # Invalid format
    response = client.get(f"/api/v1/eda/day/sc_bundle?date={date}")
    assert response.status_code == 400
    assert "Invalid date format" in response.json()["detail"]

def test_get_scatter_eda_no_data_found():
    # Choose a date far in the past or future that is unlikely to have data
    date = "2000-01-01" 
    response = client.get(f"/api/v1/eda/day/sc_bundle?date={date}")
    assert response.status_code == 404
    assert "Data not found" in response.json()["detail"]

def test_get_forecast_success():
    vehicle_id = "SM191"
    forecast_days = 7
    response = client.get(f"/api/v1/forecast/{vehicle_id}?forecast_days={forecast_days}")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == forecast_days
    assert "date" in data[0]
    assert "ensemble_forecast" in data[0]

def test_get_forecast_no_historical_data():
    # Assuming 'SM999' is a vehicle_id that doesn't exist in the data
    vehicle_id = "SM999" 
    response = client.get(f"/api/v1/forecast/{vehicle_id}")
    assert response.status_code == 404
    assert "No historical data available" in response.json()["detail"]

# This test will only pass if models are NOT trained, which is not the desired state
# For now, relying on setup_and_teardown to ensure models are trained
# def test_get_forecast_models_not_trained():
#     # To test this, you'd need to ensure models directory is empty before this test
#     # and then restore it. This fixture model isn't ideal for that.
#     vehicle_id = "SM191"
#     # Manually remove models dir for this test if possible, or create a specific fixture
#     response = client.get(f"/api/v1/forecast/{vehicle_id}")
#     assert response.status_code == 500
#     assert "Model files not found" in response.json()["detail"]
