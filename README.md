# Time Series Analysis and Forecasting

This repository contains a machine learning project for time series analysis and forecasting using multiple models such as Linear Regression, ARIMA, SARIMA, and PROPHET. The project is implemented in Python with a FastAPI application serving pre-computed EDA results and pre-trained model forecasts.

## Table of Contents

- [Time Series Analysis and Forecasting](#time-series-analysis-and-forecasting)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
    - [3. Install Dependencies](#3-install-dependencies)
  - [Project Structure](#project-structure)
  - [Usage](#usage)
    - [1. Pre-compute EDA Data](#1-pre-compute-eda-data)
    - [2. Train Machine Learning Models](#2-train-machine-learning-models)
    - [3. Run the FastAPI Application](#3-run-the-fastapi-application)
    - [4. Run Tests](#4-run-tests)
  - [Dependencies](#dependencies)
  - [License](#license)

## Installation

### 1. Clone the Repository

```sh
git clone https://github.com/TJselevani/python-analysis.git
cd python-analysis
```

### 2. Create a Virtual Environment

```sh
python -m venv venv
source venv/bin/activate  # On macOS/Linux
./venv/Scripts/activate    # On Windows
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

## Project Structure

```
├── .flake8                 # Flake8 configuration
├── .gitignore              # Git ignore file
├── config.py               # Configuration file (Pydantic BaseSettings)
├── data/                   # Directory containing raw data
│   └── last-3-months-transactions.csv
├── json/                   # Directory for pre-computed EDA JSON outputs
├── models/                 # Directory for trained machine learning models (.joblib files)
├── api/
│   ├── main.py             # FastAPI application entry point
│   └── routers/
│       ├── day_api.py      # Endpoints for daily EDA
│       └── forecast_api.py # Endpoints for forecast results
├── precompute_eda.py       # Script to pre-compute and save EDA results
├── prediction.py           # Script to load models and generate forecasts
├── requirements.txt        # List of project dependencies
├── train_models.py         # Script to train and save all machine learning models
├── tests/
│   ├── __init__.py
│   ├── conftest.py         # Pytest configuration and fixtures
│   └── test_api.py         # API tests
├── utils/                  # Helper functions and modules
│   ├── data_analysis/
│   │   └── eda.py          # EDA helper functions
│   ├── data_preparation/
│   │   ├── prepare_features.py
│   │   └── prepare_time_series.py
│   ├── ensemble/
│   │   └── ensemble_forecast.py
│   ├── forecast/
│   │   ├── create_forecast_arima.py
│   │   └── create_forecast_ml.py
│   └── model/
│       ├── arima/
│       │   └── train.py
│       ├── ml/
│       │   └── train.py
│       └── prophet/
│           └── train.py
└── README.md               # Project documentation
```

## Usage

### 1. Pre-compute EDA Data

Before running the API, you need to pre-compute the EDA data, which will be served as static JSON files.

```sh
python precompute_eda.py
```

### 2. Train Machine Learning Models

You also need to train the machine learning models. These models will be saved and then loaded by the API for making predictions.

```sh
python train_models.py
```

### 3. Run the FastAPI Application

Start the FastAPI server:

```sh
uvicorn api.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`. You can access the API documentation (Swagger UI) at `http://127.0.0.1:8000/docs`.

### 4. Run Tests

To execute the automated tests for the API:

```sh
pytest
```

## Dependencies

A list of required dependencies is available in `requirements.txt`. Key dependencies include:

- `pandas`
- `numpy`
- `scikit-learn`
- `statsmodels`
- `prophet`
- `fastapi`
- `uvicorn`
- `pydantic-settings`
- `pytest`
- `httpx`

## License

This project is open-source and available under the [MIT License](LICENSE).

---

For any issues or contributions, feel free to submit a pull request or open an issue in the repository!
