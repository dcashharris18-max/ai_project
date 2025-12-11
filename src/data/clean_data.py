"""Data cleaning and preprocessing module"""

import json
import os
from pathlib import Path

RAW_DIR = "data/raw"
CLEANED_DIR = "data/cleaned"


def clean_data(source_dir=RAW_DIR, output_dir=CLEANED_DIR):
    """
    Clean and preprocess raw data from all sources.
    
    Args:
        source_dir (str): Directory containing raw data
        output_dir (str): Directory to save cleaned data
    
    Returns:
        dict: Cleaning results summary
    """
    os.makedirs(output_dir, exist_ok=True)
    
    results = {"total_files": 0, "cleaned_files": 0}
    
    # Process all JSON files in raw directory
    for category_dir in Path(source_dir).iterdir():
        if not category_dir.is_dir():
            continue
        
        category_name = category_dir.name
        output_cat_dir = os.path.join(output_dir, category_name)
        os.makedirs(output_cat_dir, exist_ok=True)
        
        for json_file in category_dir.glob("*.json"):
            try:
                with open(json_file, "r") as f:
                    data = json.load(f)
                
                # Clean data (remove nulls, duplicates, etc.)
                if isinstance(data, list):
                    cleaned = [
                        {k: v for k, v in item.items() if v is not None}
                        for item in data
                        if isinstance(item, dict)
                    ]
                else:
                    cleaned = {k: v for k, v in data.items() if v is not None}
                
                # Save cleaned data
                output_file = os.path.join(output_cat_dir, json_file.name)
                with open(output_file, "w") as f:
                    json.dump(cleaned, f, indent=2)
                
                results["cleaned_files"] += 1
                print(f"Cleaned: {json_file.name}")
            
            except Exception as e:
                print(f"Error cleaning {json_file.name}: {e}")
            
            results["total_files"] += 1
    
    print(f"\nCleaning complete: {results['cleaned_files']}/{results['total_files']} files")
    return results


if __name__ == "__main__":
    clean_data()
