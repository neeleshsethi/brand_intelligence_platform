"""
Configuration management for the Brand Intelligence Platform.
"""

import os
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Application configuration."""

    # Project paths
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    CONFIG_DIR = BASE_DIR / "config"

    # Environment
    ENV = os.getenv("ENVIRONMENT", "development")
    DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")

    # API Configuration (if applicable)
    API_HOST = os.getenv("API_HOST", "0.0.0.0")
    API_PORT = int(os.getenv("API_PORT", "8000"))

    # Database Configuration (if applicable)
    DATABASE_URL: Optional[str] = os.getenv("DATABASE_URL")

    @classmethod
    def validate(cls) -> bool:
        """Validate configuration settings."""
        # Add validation logic here
        return True


# Create data directories if they don't exist
Config.DATA_DIR.mkdir(exist_ok=True)
(Config.DATA_DIR / "raw").mkdir(exist_ok=True)
(Config.DATA_DIR / "processed").mkdir(exist_ok=True)
