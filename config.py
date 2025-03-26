import os

# Determine the project root directory
# Assuming this script is in the root of your project
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# Construct an absolute path to the data directory
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

FILES_DIR = os.path.join(PROJECT_ROOT, "files")

# Define paths to important files
DATA_CSV_FILE = os.path.join(DATA_DIR, "last-3-months-transactions.csv")

"""
VEHICLES
- sm192
- sm944
- sm055
- sm191
- sm024
"""
