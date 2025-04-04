# flake8: noqa E501

import os
import sys

from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.notebook.convert import convert_notebooks
from logging_config import setup_logging

# convert_notebooks()
setup_logging()

from api.routers import day_api, forecast_api  # Import your routers

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with frontend URL for better security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(day_api.router)
app.include_router(forecast_api.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

# uvicorn main:app --reload
# jupyter nbconvert --to script day.ipynb
# jupyter nbconvert --to script week.ipynb
# jupyter nbconvert --to script month.ipynb
# jupyter nbconvert --to script year.ipynb
