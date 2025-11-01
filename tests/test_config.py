"""
Tests for configuration module.
"""

import pytest
from pathlib import Path

from brand_intelligence.config import Config


def test_config_base_dir_exists():
    """Test that base directory is valid."""
    assert Config.BASE_DIR.exists()
    assert Config.BASE_DIR.is_dir()


def test_config_data_dir():
    """Test that data directory is configured."""
    assert Config.DATA_DIR is not None
    assert isinstance(Config.DATA_DIR, Path)


def test_config_environment():
    """Test environment configuration."""
    assert Config.ENV in ["development", "staging", "production"]


def test_config_validation():
    """Test configuration validation."""
    assert Config.validate() is True
