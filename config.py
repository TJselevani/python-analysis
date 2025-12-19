import os
from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    # Determine the project root directory dynamically
    PROJECT_ROOT: str = os.path.dirname(os.path.abspath(__file__))

    # Construct absolute paths to important directories
    DATA_DIR: str = os.path.join(PROJECT_ROOT, "data")
    FILES_DIR: str = os.path.join(PROJECT_ROOT, "files")
    JSON_DIR: str = os.path.join(PROJECT_ROOT, "json")
    MODELS_DIR: str = os.path.join(PROJECT_ROOT, "models")

    # Define paths to important files
    DATA_CSV_FILE: str = os.path.join(DATA_DIR, "last-3-months-transactions.csv")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()

"""
VEHICLES
- sm192
- sm944
- sm055
- sm191
- sm024
"""
