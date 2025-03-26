# Time Series Analysis and Forecasting

This repository contains a machine learning project for time series analysis and forecasting using multiple models such as Linear Regression, ARIMA, SARIMA, and PROPHET. The project is implemented in Python and includes Jupyter notebooks for exploratory data analysis (EDA) and a main script (`main.py`) to run the forecasting analysis.

## Table of Contents

- [Time Series Analysis and Forecasting](#time-series-analysis-and-forecasting)
  - [Table of Contents](#table-of-contents)
  - [Installation](#installation)
    - [1. Clone the Repository](#1-clone-the-repository)
    - [2. Create a Virtual Environment](#2-create-a-virtual-environment)
    - [3. Install Dependencies](#3-install-dependencies)
  - [Project Structure](#project-structure)
  - [Usage](#usage)
  - [Exploratory Data Analysis (EDA)](#exploratory-data-analysis-eda)
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
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate    # On Windows
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

## Project Structure

```
├── config.py                 # Configuration file
├── data/                     # Directory containing raw data
├── eda/                      # Jupyter notebooks for EDA
│   ├── day.ipynb
│   ├── week.ipynb
│   ├── month.ipynb
│   ├── year.ipynb
├── files/                    # Directory for storing analysis files
├── main.py                    # Main script for running forecasting
├── main.ipynb                 # Jupyter notebook version of the main script
├── utils/                     # Helper functions
│   ├── data_preparation/
│   │   ├── prepare_time_series.py
│   ├── ensemble/
│   │   ├── ensemble_forecast.py
│   │   ├── plot_ensemble_forecast.py
│   ├── prediction/
│   │   ├── ensemble_prediction.py
├── requirements.txt           # List of dependencies
├── README.md                  # Project documentation
```

## Usage

To run the time series forecasting analysis, execute the `main.py` script:

```sh
python main.py
```

This script:

1. Loads the dataset from `config.py`.
2. Runs predictions using different models.
3. Creates an ensemble forecast.
4. Visualizes and prints the forecast for the next 7 days.

## Exploratory Data Analysis (EDA)

The `eda/` directory contains Jupyter notebooks for data visualization:

- `day.ipynb`: Analysis at the daily level.
- `week.ipynb`: Weekly trends.
- `month.ipynb`: Monthly patterns.
- `year.ipynb`: Yearly trends.

To run the EDA notebooks:

```sh
jupyter notebook
```

Then open the desired notebook from the `eda/` directory.

## Dependencies

A list of required dependencies is available in `requirements.txt`. The major dependencies include:

- `pandas`
- `numpy`
- `matplotlib`
- `seaborn`
- `scikit-learn`
- `statsmodels`
- `prophet`
- `plotly`
- `jupyter`

## License

This project is open-source and available under the [MIT License](LICENSE).

---

For any issues or contributions, feel free to submit a pull request or open an issue in the repository!
