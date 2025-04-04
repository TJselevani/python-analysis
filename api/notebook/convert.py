import os
import sys
import subprocess

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from config import NOTEBOOKS_DIR, SCRIPTS_DIR

# Ensure the output directory exists
os.makedirs(SCRIPTS_DIR, exist_ok=True)


def convert_notebooks():
    """Converts all .ipynb files in NOTEBOOKS_DIR to .py and saves them in OUTPUT_DIR."""
    for notebook in ["day.ipynb", "week.ipynb", "month.ipynb", "year.ipynb"]:
        input_path = os.path.join(NOTEBOOKS_DIR, notebook)
        output_path = os.path.join(SCRIPTS_DIR, notebook.replace(".ipynb", ".py"))

        if os.path.exists(input_path):
            cmd = f'jupyter nbconvert --to script "{input_path}" --output-dir="{SCRIPTS_DIR}"'
            subprocess.run(cmd, shell=True, check=True)
            print(f"Converted: {notebook} -> {output_path}")
        else:
            print(f"Skipping: {notebook} (File not found)")
