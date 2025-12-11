"""Data tokenization and encoding module"""

import json
import os
import pickle
from pathlib import Path
import torch

CLEANED_DIR = "data/cleaned"
TOKENIZED_DIR = "data/tokenized"


def tokenize_data(source_dir=CLEANED_DIR, output_dir=TOKENIZED_DIR):
    """
    Tokenize and encode cleaned data for model training.
    
    Args:
        source_dir (str): Directory containing cleaned data
        output_dir (str): Directory to save tokenized data
    
    Returns:
        dict: Tokenization results summary
    """
    os.makedirs(output_dir, exist_ok=True)
    
    results = {"total_files": 0, "tokenized_files": 0}
    
    # Process all JSON files in cleaned directory
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
                
                # Convert to tensor format (simplified tokenization)
                if isinstance(data, list):
                    # Extract numeric values for tensor conversion
                    tokens = []
                    for item in data:
                        if isinstance(item, dict):
                            numeric_vals = [
                                float(v) if isinstance(v, (int, float)) else 0
                                for v in item.values()
                            ]
                            tokens.append(numeric_vals)
                    
                    tokens_tensor = torch.FloatTensor(tokens) if tokens else torch.tensor([])
                else:
                    # Handle dict data
                    numeric_vals = [
                        float(v) if isinstance(v, (int, float)) else 0
                        for v in data.values()
                    ]
                    tokens_tensor = torch.FloatTensor([numeric_vals])
                
                # Save tokenized data
                output_file = os.path.join(
                    output_cat_dir,
                    json_file.stem + "_tokens.pt"
                )
                torch.save(tokens_tensor, output_file)
                
                results["tokenized_files"] += 1
                print(f"Tokenized: {json_file.name} -> {tokens_tensor.shape}")
            
            except Exception as e:
                print(f"Error tokenizing {json_file.name}: {e}")
            
            results["total_files"] += 1
    
    print(f"\nTokenization complete: {results['tokenized_files']}/{results['total_files']} files")
    return results


if __name__ == "__main__":
    tokenize_data()
