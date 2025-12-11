"""E-commerce product data fetching module"""

import json
import os
from datetime import datetime

OUTDIR = "data/raw/ecommerce"


def fetch_products_data(category="electronics", limit=100):
    """
    Fetch e-commerce product data.
    
    Args:
        category (str): Product category
        limit (int): Number of products to fetch
    
    Returns:
        list: List of product records
    """
    os.makedirs(OUTDIR, exist_ok=True)
    
    # Placeholder for product data fetching logic
    data = [
        {
            "id": f"product_{i}",
            "timestamp": datetime.now().isoformat(),
            "category": category,
            "name": f"Product {i}",
            "price": 10.0 + (i * 5),
            "reviews": i,
        }
        for i in range(limit)
    ]
    
    output_file = os.path.join(OUTDIR, f"{category}_products.json")
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved {len(data)} products from {category}")
    return data


if __name__ == "__main__":
    fetch_products_data()
