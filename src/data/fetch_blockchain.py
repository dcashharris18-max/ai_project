"""Blockchain data fetching module"""

import json
import os
from datetime import datetime

OUTDIR = "data/raw/blockchain"


def fetch_blockchain_data(network="ethereum", limit=100):
    """
    Fetch blockchain data from specified network.
    
    Args:
        network (str): Blockchain network (ethereum, bitcoin, etc.)
        limit (int): Number of records to fetch
    
    Returns:
        list: List of blockchain records
    """
    os.makedirs(OUTDIR, exist_ok=True)
    
    # Placeholder for blockchain data fetching logic
    data = [
        {
            "timestamp": datetime.now().isoformat(),
            "network": network,
            "block_height": i,
            "transactions": i * 100,
        }
        for i in range(limit)
    ]
    
    output_file = os.path.join(OUTDIR, f"{network}_data.json")
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved {len(data)} blockchain records for {network}")
    return data


if __name__ == "__main__":
    fetch_blockchain_data()
