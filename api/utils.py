# utils.py
import os
import json
import asyncio
import aiofiles
import logging
from functools import wraps
from logging.handlers import RotatingFileHandler
from fastapi import HTTPException

# Setup rotating logger
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "app.log")

logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.INFO)

handler = RotatingFileHandler(log_path, maxBytes=2_000_000, backupCount=5)
formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)


def ensure_directory_exists(file_path: str):
    """Ensure directory for the file exists."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)


def log_and_handle_file_generation(generate_method):
    """
    Decorator to wrap endpoints that:
    - generate and read a file (if missing)
    - auto-create directories
    - log all steps
    """

    @wraps(generate_method)
    async def wrapper(*args, **kwargs):
        file_path = kwargs.get("file_path")
        if not file_path:
            raise HTTPException(
                status_code=500, detail="No file_path provided to decorator"
            )

        logger.info(f"Request received: {file_path}")

        try:
            if not os.path.exists(file_path):
                logger.info(f"File not found. Generating: {file_path}")
                ensure_directory_exists(file_path)

                # Run generation method in a thread
                await asyncio.to_thread(generate_method)

                # Wait briefly for file generation
                for _ in range(20):
                    if os.path.exists(file_path):
                        break
                    await asyncio.sleep(0.1)

            if not os.path.exists(file_path):
                msg = f"File still missing after generation: {file_path}"
                logger.error(msg)
                raise HTTPException(status_code=500, detail=msg)

            # Read and return JSON content
            async with aiofiles.open(file_path, mode="r", encoding="utf-8") as f:
                content = await f.read()
                logger.info(f"Successfully read file: {file_path}")
                return json.loads(content)

        except Exception as e:
            logger.exception(f"Exception during file generation or reading: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error processing file: {e}")

    return wrapper
