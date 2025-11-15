# CLAUDE.md - AI Assistant Guide

**Last Updated**: 2025-11-15
**Project Version**: 0.1.0
**Status**: Alpha - Early Development Stage

---

## Project Overview

The **Brand Intelligence Platform** is a comprehensive data platform designed for monitoring, analyzing, and reporting on brand performance, sentiment, and competitive intelligence across multiple channels. This is an early-stage Python project (v0.1.0) with a solid foundation ready for feature development.

### Core Features (Planned)
- Brand sentiment analysis
- Social media monitoring
- Competitor tracking
- Multi-channel data aggregation
- Real-time analytics and reporting
- Custom dashboards and visualizations

### Current State
The project currently has:
- Well-structured foundation with configuration management
- Testing infrastructure in place
- Code quality tools configured
- Modular architecture ready for expansion

---

## Codebase Structure

```
/home/user/brand_intelligence_platform/
├── src/
│   └── brand_intelligence/           # Main Python package
│       ├── __init__.py               # Package initialization (version 0.1.0)
│       ├── config.py                 # Configuration management (CRITICAL)
│       └── main.py                   # Application entry point
├── tests/
│   ├── __init__.py
│   └── test_config.py                # Configuration tests (4 tests)
├── config/                           # Configuration files directory (empty template)
├── data/                             # Data storage (gitignored)
│   ├── raw/                          # Raw data storage (auto-created)
│   └── processed/                    # Processed data storage (auto-created)
├── docs/                             # Documentation directory
├── .env.example                      # Environment variables template
├── .gitignore                        # Git exclusions (comprehensive)
├── README.md                         # User-facing documentation
├── CLAUDE.md                         # This file - AI assistant guide
├── requirements.txt                  # Python dependencies
└── pyproject.toml                    # Project configuration & metadata
```

---

## Technology Stack

### Core Technologies
- **Python 3.9+** (supports 3.9, 3.10, 3.11)
- **requests** (>=2.31.0) - HTTP library for API calls
- **pandas** (>=2.0.0) - Data manipulation and analysis
- **numpy** (>=1.24.0) - Numerical computing
- **python-dotenv** (>=1.0.0) - Environment variable management

### Web Framework (Ready for Use)
- **FastAPI** (>=0.100.0) - Modern async web framework
- **Uvicorn** (>=0.23.0) - ASGI application server

### Database (Ready for Use)
- **SQLAlchemy** (>=2.0.0) - ORM for database abstraction

### Development Tools
- **pytest** (>=7.4.0) - Testing framework
- **pytest-cov** (>=4.1.0) - Code coverage reporting
- **black** (>=23.0.0) - Code formatter
- **flake8** (>=6.0.0) - Style checker
- **mypy** (>=1.5.0) - Static type checker

---

## Key Files and Their Purposes

### Configuration Files

#### `/pyproject.toml` - Primary Project Configuration
**Location**: `/home/user/brand_intelligence_platform/pyproject.toml`
**Purpose**: Modern Python project configuration using setuptools

**Key Settings**:
- **Black**: 100-character line length (NOT 88)
- **Pytest**: Looks for `test_*.py` files in `tests/` directory
- **MyPy**: Strict type checking enabled, Python 3.9 target
- **Build System**: setuptools>=68.0.0, wheel support

**When to Modify**:
- Adding new dependencies (update `dependencies` list)
- Changing code quality tool settings
- Updating project metadata

#### `/requirements.txt` - Dependency List
**Location**: `/home/user/brand_intelligence_platform/requirements.txt`
**Purpose**: Lists all project dependencies with version constraints

**When to Modify**:
- Installing new packages
- Updating package versions
- After modifying pyproject.toml dependencies

**Important**: Keep in sync with pyproject.toml dependencies

#### `/.env.example` - Environment Variables Template
**Location**: `/home/user/brand_intelligence_platform/.env.example`
**Purpose**: Template for environment variables

**Variables Defined**:
```env
ENVIRONMENT=development|staging|production
DEBUG=True|False
API_HOST=0.0.0.0
API_PORT=8000
DATABASE_URL=postgresql://user:password@localhost:5432/brand_intelligence
SOCIAL_MEDIA_API_KEY=your_key_here
ANALYTICS_API_SECRET=your_secret_here
```

**Important**: Never commit actual `.env` files (gitignored)

### Source Code Files

#### `/src/brand_intelligence/config.py` - Configuration Management
**Location**: `/home/user/brand_intelligence_platform/src/brand_intelligence/config.py:1`
**Purpose**: Centralized configuration management (SINGLETON PATTERN)

**Key Features**:
- Loads environment variables via `python-dotenv`
- Defines project paths (BASE_DIR, DATA_DIR, CONFIG_DIR)
- API configuration (host, port)
- Database URL configuration
- Auto-creates data subdirectories on import
- Includes `validate()` method for config validation

**Critical Details**:
- Uses `pathlib.Path` for cross-platform compatibility
- `BASE_DIR = Path(__file__).parent.parent.parent` (3 levels up)
- Auto-creates `data/raw/` and `data/processed/` directories
- Singleton pattern with class-level attributes

**When to Modify**:
- Adding new configuration variables
- Adding new path definitions
- Extending validation logic in `validate()` method

#### `/src/brand_intelligence/main.py` - Application Entry Point
**Location**: `/home/user/brand_intelligence_platform/src/brand_intelligence/main.py:1`
**Purpose**: Main application initialization

**Current Functionality** (lines 8-16):
- Displays version, environment, and data directory
- Imports Config class
- Placeholder for initialization logic

**When to Modify**:
- Adding application startup logic
- Initializing services
- Setting up logging
- Creating main application flow

#### `/src/brand_intelligence/__init__.py` - Package Initialization
**Location**: `/home/user/brand_intelligence_platform/src/brand_intelligence/__init__.py:1`
**Purpose**: Package metadata and exports

**Current Content**:
- `__version__ = "0.1.0"`
- Module docstring
- Author placeholder

**When to Modify**:
- Updating version number
- Exporting public API
- Adding package-level imports

### Testing Files

#### `/tests/test_config.py` - Configuration Tests
**Location**: `/home/user/brand_intelligence_platform/tests/test_config.py:1`
**Purpose**: Unit tests for configuration module

**Current Tests** (4 total):
1. `test_config_base_dir_exists()` - Validates BASE_DIR exists
2. `test_config_data_dir()` - Validates DATA_DIR configuration
3. `test_config_environment()` - Validates ENV is valid
4. `test_config_validation()` - Tests validate() method

**Testing Pattern**:
- Uses pytest framework
- Tests are descriptive with docstrings
- Covers path validation and environment checks

---

## Development Workflows

### Environment Setup

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate virtual environment
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create .env file from template
cp .env.example .env
# Edit .env with your actual values

# 5. Run tests to verify setup
pytest tests/
```

### Running the Application

```bash
# Activate virtual environment first
source venv/bin/activate

# Run main application
python -m brand_intelligence.main

# Expected output:
# Brand Intelligence Platform v0.1.0
# Environment: development
# Data directory: /path/to/brand_intelligence_platform/data
# Platform initialized successfully!
```

### Testing Workflow

```bash
# Run all tests
pytest tests/

# Run with coverage
pytest --cov=brand_intelligence tests/

# Run specific test file
pytest tests/test_config.py

# Run specific test function
pytest tests/test_config.py::test_config_base_dir_exists

# Run with verbose output
pytest -v tests/
```

### Code Quality Workflow

```bash
# Format code with Black (100-char line length)
black src/

# Check code style with flake8
flake8 src/

# Type check with mypy (strict mode)
mypy src/

# Run all quality checks before committing
black src/ && flake8 src/ && mypy src/ && pytest tests/
```

### Git Workflow

Current branch: `claude/claude-md-mhzqzd41sf9gebnu-011RykUfTY1TJfLghtPUieKf`

```bash
# Check status
git status

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add feature description"

# Push to current branch
git push -u origin claude/claude-md-mhzqzd41sf9gebnu-011RykUfTY1TJfLghtPUieKf
```

**Commit Message Conventions**:
- `feat:` - New feature
- `fix:` - Bug fix
- `refactor:` - Code refactoring
- `test:` - Adding/updating tests
- `docs:` - Documentation changes
- `chore:` - Maintenance tasks

---

## Code Quality Standards

### Type Checking (MyPy - Strict Mode)

**Configuration** (pyproject.toml:49-53):
```toml
[tool.mypy]
python_version = "3.9"
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
```

**Requirements**:
- ALL functions must have type hints for parameters and return values
- Use `Optional[Type]` for nullable values
- Import types from `typing` module as needed

**Example**:
```python
from typing import Optional, List, Dict

def process_data(data: List[Dict[str, str]], max_items: Optional[int] = None) -> bool:
    """Process data with type hints."""
    # Implementation
    return True
```

### Code Formatting (Black)

**Configuration** (pyproject.toml:39-41):
```toml
[tool.black]
line-length = 100
target-version = ['py39', 'py310', 'py311']
```

**Important**: Line length is **100 characters**, NOT the default 88

**Usage**:
```bash
black src/  # Format all files
black --check src/  # Check without modifying
```

### Style Checking (Flake8)

**Usage**:
```bash
flake8 src/
```

**Common Issues to Avoid**:
- Unused imports
- Undefined variables
- Line too long (>100 chars after Black should be rare)
- Missing whitespace

### Testing Standards (Pytest)

**Configuration** (pyproject.toml:43-47):
```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
```

**Testing Patterns**:
- Test files: `test_*.py` in `tests/` directory
- Test functions: `test_*` with descriptive names
- Include docstrings explaining what each test validates
- Use pytest fixtures for setup/teardown
- Aim for high coverage (use pytest-cov)

**Example**:
```python
"""Tests for new module."""

import pytest

def test_function_name():
    """Test that function does X correctly."""
    result = function_under_test()
    assert result == expected_value
```

---

## Architectural Patterns and Conventions

### 1. Singleton Configuration Pattern

**Location**: `/src/brand_intelligence/config.py`

The `Config` class uses a singleton pattern with class-level attributes:

```python
class Config:
    """Application configuration."""

    # Class-level attributes (shared across all instances)
    BASE_DIR = Path(__file__).parent.parent.parent
    DATA_DIR = BASE_DIR / "data"
    ENV = os.getenv("ENVIRONMENT", "development")

    @classmethod
    def validate(cls) -> bool:
        """Validate configuration settings."""
        return True
```

**Usage**:
```python
from brand_intelligence.config import Config

# Access directly via class (no instantiation needed)
print(Config.ENV)
print(Config.DATA_DIR)
```

**Why**: Single source of truth for all configuration, loaded once on import

### 2. Path-Based File Organization

**Pattern**: Use `pathlib.Path` for ALL file/directory operations

**Example**:
```python
from pathlib import Path

# Good
data_file = Config.DATA_DIR / "raw" / "data.csv"
if data_file.exists():
    data = pd.read_csv(data_file)

# Avoid
data_file = Config.DATA_DIR + "/raw/data.csv"  # String concatenation
```

**Benefits**:
- Cross-platform compatibility (Windows/Linux/Mac)
- Cleaner syntax with `/` operator
- Built-in file operations (exists(), mkdir(), read_text(), etc.)

### 3. Separation of Concerns

**Current Structure**:
- **Configuration**: Isolated in `config.py`
- **Application Logic**: In domain-specific modules (to be added)
- **Entry Point**: `main.py` (orchestration only)
- **Tests**: Parallel structure in `tests/` directory

**When Adding New Features**:
```
src/brand_intelligence/
├── config.py              # Configuration only
├── main.py                # Entry point only
├── models/                # Data models
│   └── sentiment.py
├── services/              # Business logic
│   └── sentiment_analyzer.py
├── api/                   # API endpoints
│   └── routes.py
└── utils/                 # Utility functions
    └── helpers.py
```

### 4. Environment-Based Configuration

**Pattern**: All environment-specific settings go in `.env` file

**Configuration Levels**:
1. **Defaults in code**: `Config.API_HOST = os.getenv("API_HOST", "0.0.0.0")`
2. **Environment variables**: `.env` file (development)
3. **System environment**: Production servers

**Example**:
```python
# config.py
API_KEY = os.getenv("API_KEY")  # No default - REQUIRED
DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1", "yes")  # Default provided
```

### 5. Auto-Directory Creation

**Pattern**: Directories created automatically when needed

**Current Implementation** (config.py:41-44):
```python
# Create data directories if they don't exist
Config.DATA_DIR.mkdir(exist_ok=True)
(Config.DATA_DIR / "raw").mkdir(exist_ok=True)
(Config.DATA_DIR / "processed").mkdir(exist_ok=True)
```

**When Adding New Directories**:
- Add creation logic in `config.py` if needed on startup
- Use `exist_ok=True` to avoid errors if already exists
- Use `parents=True` if creating nested directories

---

## Common Tasks for AI Assistants

### Adding a New Module

1. **Create module file** in `src/brand_intelligence/`
2. **Add type hints** to all functions (mypy strict mode)
3. **Create corresponding test file** in `tests/`
4. **Update imports** if needed in `__init__.py`
5. **Run quality checks**: `black src/ && flake8 src/ && mypy src/ && pytest tests/`

**Example**:
```python
# src/brand_intelligence/sentiment_analyzer.py
"""Sentiment analysis module."""

from typing import Dict, List

def analyze_sentiment(text: str) -> Dict[str, float]:
    """
    Analyze sentiment of given text.

    Args:
        text: Input text to analyze

    Returns:
        Dictionary with sentiment scores
    """
    # Implementation
    return {"positive": 0.8, "negative": 0.1, "neutral": 0.1}
```

```python
# tests/test_sentiment_analyzer.py
"""Tests for sentiment analyzer."""

import pytest
from brand_intelligence.sentiment_analyzer import analyze_sentiment

def test_analyze_sentiment():
    """Test that sentiment analysis returns valid scores."""
    result = analyze_sentiment("This is great!")
    assert "positive" in result
    assert result["positive"] > 0
```

### Adding Configuration Variables

1. **Add to `.env.example`** with documentation
2. **Add to `Config` class** in `config.py`
3. **Add validation** in `Config.validate()` if required
4. **Add test** in `test_config.py`
5. **Document** in this CLAUDE.md file

**Example**:
```python
# .env.example
SOCIAL_MEDIA_API_KEY=your_api_key_here

# config.py
class Config:
    SOCIAL_MEDIA_API_KEY: Optional[str] = os.getenv("SOCIAL_MEDIA_API_KEY")

    @classmethod
    def validate(cls) -> bool:
        """Validate configuration settings."""
        if cls.ENV == "production" and not cls.SOCIAL_MEDIA_API_KEY:
            raise ValueError("SOCIAL_MEDIA_API_KEY required in production")
        return True

# tests/test_config.py
def test_social_media_api_key():
    """Test that social media API key is configured."""
    # Test logic here
```

### Adding Dependencies

1. **Add to `requirements.txt`** with version constraint
2. **Add to `pyproject.toml`** in `dependencies` list
3. **Install in venv**: `pip install package_name`
4. **Test import** in code
5. **Run tests** to ensure nothing breaks

**Example**:
```bash
# Add to requirements.txt
beautifulsoup4>=4.12.0

# Add to pyproject.toml
dependencies = [
    "requests>=2.31.0",
    "beautifulsoup4>=4.12.0",  # Add here
    # ...
]

# Install
pip install beautifulsoup4>=4.12.0

# Verify
python -c "import bs4; print(bs4.__version__)"
```

### Creating API Endpoints (FastAPI)

FastAPI is already in dependencies but not yet configured. When implementing:

1. **Create `api/` directory** in `src/brand_intelligence/`
2. **Create `routes.py`** for endpoints
3. **Update `main.py`** to initialize FastAPI app
4. **Add tests** in `tests/test_api.py`

**Example Structure**:
```python
# src/brand_intelligence/api/routes.py
"""API routes for brand intelligence platform."""

from fastapi import APIRouter

router = APIRouter()

@router.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint."""
    return {"status": "healthy"}
```

### Working with Data Files

**Pattern**: All data goes in `data/` directory (gitignored)

**Structure**:
- `data/raw/` - Original, immutable data
- `data/processed/` - Cleaned, transformed data

**Example**:
```python
from brand_intelligence.config import Config
import pandas as pd

# Reading raw data
raw_data_path = Config.DATA_DIR / "raw" / "social_media.csv"
df = pd.read_csv(raw_data_path)

# Processing and saving
processed_data_path = Config.DATA_DIR / "processed" / "social_media_clean.csv"
df_clean.to_csv(processed_data_path, index=False)
```

**Important**: Data files are gitignored - never commit to repository

---

## File Naming Conventions

### Python Files
- **Modules**: `lowercase_with_underscores.py` (snake_case)
- **Test files**: `test_module_name.py`
- **Private modules**: `_internal_module.py` (prefix with underscore)

### Functions and Variables
- **Functions**: `lowercase_with_underscores()` (snake_case)
- **Variables**: `lowercase_with_underscores` (snake_case)
- **Constants**: `UPPERCASE_WITH_UNDERSCORES` (SCREAMING_SNAKE_CASE)
- **Classes**: `CapitalizedWords` (PascalCase)
- **Private**: `_leading_underscore` for internal use

### Examples
```python
# Good
class SentimentAnalyzer:
    MAX_RETRIES = 3

    def __init__(self):
        self._cache = {}

    def analyze_text(self, input_text: str) -> float:
        """Analyze text sentiment."""
        pass

# Avoid
class sentimentAnalyzer:  # Wrong case
    maxRetries = 3  # Should be constant

    def AnalyzeText(self, InputText):  # Wrong case
        pass
```

---

## .gitignore Rules

**Location**: `/.gitignore`

**Critical Exclusions**:
- `.env` files (NEVER commit secrets)
- `data/` directory contents (large files, PII)
- `__pycache__/` and `*.pyc` (Python artifacts)
- Virtual environments (`venv/`, `env/`)
- IDE files (`.vscode/`, `.idea/`)
- Test artifacts (`.pytest_cache/`, `.coverage`)

**What IS Committed**:
- Source code (`src/`)
- Tests (`tests/`)
- Configuration templates (`.env.example`)
- Documentation (`README.md`, `CLAUDE.md`)
- Dependency lists (`requirements.txt`, `pyproject.toml`)

---

## Directory Auto-Creation

**Current Auto-Created Directories** (on config.py import):
- `data/`
- `data/raw/`
- `data/processed/`

**Implementation** (config.py:41-44):
```python
Config.DATA_DIR.mkdir(exist_ok=True)
(Config.DATA_DIR / "raw").mkdir(exist_ok=True)
(Config.DATA_DIR / "processed").mkdir(exist_ok=True)
```

**When to Add More**:
- Directories needed for application to function
- Directories that should exist even if empty
- Output directories for reports, logs, etc.

---

## Important Notes for AI Assistants

### When Making Changes

1. **Always run tests** before and after changes: `pytest tests/`
2. **Format code** with Black: `black src/`
3. **Type check** with mypy: `mypy src/`
4. **Update tests** when changing functionality
5. **Update this CLAUDE.md** if architecture changes

### Code Style Preferences

- **Line length**: 100 characters (NOT 88)
- **Type hints**: REQUIRED on all functions (mypy strict mode)
- **Docstrings**: Use for all public functions and classes
- **Imports**: Organize as: stdlib, third-party, local
- **Path handling**: Always use `pathlib.Path`, never string concatenation

### Common Pitfalls to Avoid

1. **Don't commit `.env` files** - Always use `.env.example` as template
2. **Don't commit data files** - Use `data/` directory (gitignored)
3. **Don't skip type hints** - mypy strict mode will fail
4. **Don't use 88-char line length** - Black configured for 100
5. **Don't modify `Config` class without updating tests**
6. **Don't add dependencies without updating both** `requirements.txt` AND `pyproject.toml`

### Testing Philosophy

- **Write tests FIRST** when possible (TDD)
- **Test behavior, not implementation**
- **Use descriptive test names** that explain what's being tested
- **Include docstrings** in test functions
- **Aim for high coverage** but don't sacrifice quality for 100%

### When Stuck or Unsure

1. **Check existing patterns** in codebase
2. **Run tests** to understand current behavior
3. **Read configuration** in `pyproject.toml`
4. **Check environment variables** in `.env.example`
5. **Validate assumptions** with small test scripts

---

## Future Development Guidelines

### Planned Features to Implement

Based on README.md and current setup, the following features are planned:

1. **Brand Sentiment Analysis** - Analyze brand mentions for sentiment
2. **Social Media Monitoring** - Track brand mentions across platforms
3. **Competitor Tracking** - Monitor competitor activities
4. **Multi-Channel Data Aggregation** - Collect data from various sources
5. **Real-Time Analytics** - Process and analyze data in real-time
6. **Custom Dashboards** - Visualize data and insights

### Suggested Architecture for Features

```
src/brand_intelligence/
├── config.py                      # Existing
├── main.py                        # Existing
├── models/                        # Data models
│   ├── __init__.py
│   ├── brand.py
│   ├── sentiment.py
│   └── competitor.py
├── services/                      # Business logic
│   ├── __init__.py
│   ├── sentiment_analyzer.py
│   ├── social_media_monitor.py
│   └── competitor_tracker.py
├── data_sources/                  # Data collection
│   ├── __init__.py
│   ├── twitter_collector.py
│   ├── reddit_collector.py
│   └── news_collector.py
├── api/                           # FastAPI endpoints
│   ├── __init__.py
│   ├── routes.py
│   └── dependencies.py
├── database/                      # Database models & migrations
│   ├── __init__.py
│   └── models.py
└── utils/                         # Utility functions
    ├── __init__.py
    └── text_processing.py
```

### When Adding Database Support

SQLAlchemy is already in dependencies:

1. **Create database models** in `database/models.py`
2. **Add DATABASE_URL** to `.env` (already in template)
3. **Create database initialization** in `database/__init__.py`
4. **Add migrations** (consider alembic)
5. **Update tests** with database fixtures

### When Adding API Endpoints

FastAPI and Uvicorn are already in dependencies:

1. **Create `api/` module** with routes
2. **Update `main.py`** to create FastAPI app
3. **Add API tests** using FastAPI TestClient
4. **Document endpoints** with FastAPI automatic docs
5. **Add authentication** if needed

---

## Quick Reference

### Essential Commands
```bash
# Setup
python -m venv venv && source venv/bin/activate && pip install -r requirements.txt

# Run application
python -m brand_intelligence.main

# Run tests
pytest tests/

# Code quality (run before commit)
black src/ && flake8 src/ && mypy src/ && pytest tests/

# Coverage report
pytest --cov=brand_intelligence --cov-report=html tests/
```

### Essential Paths
```python
from brand_intelligence.config import Config

Config.BASE_DIR    # /home/user/brand_intelligence_platform
Config.DATA_DIR    # /home/user/brand_intelligence_platform/data
Config.CONFIG_DIR  # /home/user/brand_intelligence_platform/config
```

### Essential Imports
```python
# Configuration
from brand_intelligence.config import Config

# Type hints
from typing import Optional, List, Dict, Any, Union

# Path handling
from pathlib import Path

# Environment variables
import os
from dotenv import load_dotenv
```

---

## Contact and Support

For questions about this codebase:
1. Check this CLAUDE.md file first
2. Review README.md for user-facing documentation
3. Check test files for usage examples
4. Review pyproject.toml for configuration

---

**END OF CLAUDE.md**

*This file should be updated whenever significant architectural changes are made to the codebase.*
