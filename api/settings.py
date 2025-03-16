import logging
import os
from pathlib import Path

from dotenv import load_dotenv

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).parent.parent
load_dotenv(BASE_DIR / ".env")


def get_env(key, default=None, as_type=str):
    value = os.getenv(key, None)
    if value is None:
        if default is not None:
            value = default
        else:
            raise ValueError(f"""
Missing required variable in .env file:

{key}

Please make sure your .env file is correct.""")
    return as_type(value)


DEBUG = get_env("DEBUG", default=False)

ANTHROPIC_API_KEY: str = get_env("ANTHROPIC_API_KEY")
