"""Main entry point for AI project pipeline"""

import os
import sys
from pathlib import Path

from src.data.fetch_products import fetch_products_data

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from src.data import (
    fetch_blockchain_data,
    fetch_crypto_data,
    fetch_social_data,
    fetch_products_data,
)
from src.models import ModelManager


def main():
    """
    Main pipeline execution.
    
    Workflow:
    1. Fetch data from all sources
    2. Clean and preprocess data
    3. Tokenize data for model training
    4. Prepare for model training
    """
    
    print("=" * 60)
    print("AI Project Data Pipeline")
    print("=" * 60)
    
    # Step 1: Fetch data from all sources
    print("\n[Step 1] Fetching data from all sources...")
    
    try:
        print("\n  - Fetching blockchain data...")
        fetch_blockchain_data(limit=50)
    except Exception as e:
        print(f"  - Blockchain fetch error: {e}")
    
    try:
        print("\n  - Fetching cryptocurrency data...")
        fetch_crypto_data(symbol="BTC/USDT", limit=100)
    except Exception as e:
        print(f"  - Crypto fetch error: {e}")
    
    try:
        print("\n  - Fetching social media data...")
        fetch_social_data(limit=50)
    except Exception as e:
        print(f"  - Social data fetch error: {e}")
    
    try:
        print("\n  - Fetching e-commerce product data...")
        fetch_products_data(limit=50)
    except Exception as e:
        print(f"  - Product data fetch error: {e}")
    
    # Step 2: Clean data
    print("\n[Step 2] Cleaning data...")
    print("  (Data cleaning not yet implemented)")
    
    # Step 3: Tokenize data
    print("\n[Step 3] Tokenizing data...")
    print("  (Data tokenization not yet implemented)")
    
    # Step 4: Model management setup
    print("\n[Step 4] Setting up model management...")
    try:
        manager = ModelManager()
        print(f"  Available models: {manager.list_models()}")
    except Exception as e:
        print(f"  Model manager error: {e}")
    
    print("\n" + "=" * 60)
    print("Pipeline complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
