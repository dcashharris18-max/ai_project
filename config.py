"""Project configuration and settings"""

import os
from pathlib import Path

# Project directories
PROJECT_ROOT = Path(__file__).parent
SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
MODELS_DIR = PROJECT_ROOT / "Models"

# Data directories
RAW_DATA_DIR = DATA_DIR / "raw"
CLEANED_DATA_DIR = DATA_DIR / "cleaned"
TOKENIZED_DATA_DIR = DATA_DIR / "tokenized"

# Create directories if they don't exist
for directory in [RAW_DATA_DIR, CLEANED_DATA_DIR, TOKENIZED_DATA_DIR]:
    directory.mkdir(parents=True, exist_ok=True)

# Data sources
DATA_SOURCES = {
    "blockchain": {
        "enabled": True,
        "output_dir": RAW_DATA_DIR / "blockchain",
    },
    "crypto": {
        "enabled": True,
        "output_dir": RAW_DATA_DIR / "crypto",
        "symbol": "BTC/USDT",
        "timeframe": "1h",
        "limit": 500,
    },
    "social": {
        "enabled": True,
        "output_dir": RAW_DATA_DIR / "social",
        "platform": "reddit",
        "limit": 100,
    },
    "ecommerce": {
        "enabled": True,
        "output_dir": RAW_DATA_DIR / "ecommerce",
        "limit": 100,
    },
}

# Model settings
MODEL_SETTINGS = {
    "model_dir": MODELS_DIR,
    "device": "cuda",  # or "cpu"
    "learning_rate": 0.001,
    "epochs": 10,
    "batch_size": 32,
}

# Processing settings
PROCESSING_SETTINGS = {
    "raw_data_dir": RAW_DATA_DIR,
    "cleaned_data_dir": CLEANED_DATA_DIR,
    "tokenized_data_dir": TOKENIZED_DATA_DIR,
    "remove_nulls": True,
    "remove_duplicates": True,
}

# Logging
LOG_LEVEL = "INFO"
LOG_FILE = PROJECT_ROOT / "logs" / "project.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)

print(f"Project root: {PROJECT_ROOT}")
print(f"Data directory: {DATA_DIR}")
print(f"Models directory: {MODELS_DIR}")
