# flake8: noqa E501
import os
import sys
import pandas as pd
from datetime import timedelta

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import settings
from utils.data_analysis.eda import load_and_prepare_data, generate_day_scatter_json

def precompute_all_eda_data():
    """
    Loads the data and runs all EDA pre-computation functions.
    """
    print("Starting EDA pre-computation...")
    data = load_and_prepare_data(settings.DATA_CSV_FILE)
    
    unique_dates = data['date'].unique()
    unique_vehicles = data['vehicle_booked'].dropna().unique()

    # Generate scatter plots for each date and each vehicle
    for date_obj in unique_dates:
        date_str = date_obj.strftime('%Y-%m-%d')
        
        # For all vehicles combined
        generate_day_scatter_json(data, date_str, settings.JSON_DIR)
        
        # For each individual vehicle
        for vehicle_id in unique_vehicles:
            generate_day_scatter_json(data, date_str, settings.JSON_DIR, vehicle_id=vehicle_id)

    print("EDA pre-computation finished.")

if __name__ == "__main__":
    precompute_all_eda_data()
