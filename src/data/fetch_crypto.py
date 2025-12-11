"""Cryptocurrency data fetching module"""

import ccxt
import json
import os
from datetime import datetime

OUTDIR = "data/raw/crypto"


def fetch_crypto_data(symbol="BTC/USDT", timeframe="1h", limit=500):
    """
    Fetch cryptocurrency OHLCV data using CCXT.
    
    Args:
        symbol (str): Trading pair symbol (e.g., "BTC/USDT")
        timeframe (str): Candle timeframe (1m, 5m, 1h, 1d, etc.)
        limit (int): Number of candles to fetch
    
    Returns:
        list: List of OHLCV records
    """
    os.makedirs(OUTDIR, exist_ok=True)
    
    exchange = ccxt.binance()
    ohlcv = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
    
    data = []
    for candle in ohlcv:
        ts, o, h, l, c, v = candle
        data.append({
            "timestamp": ts,
            "datetime": datetime.utcfromtimestamp(ts/1000).isoformat(),
            "open": o,
            "high": h,
            "low": l,
            "close": c,
            "volume": v
        })
    
    output_file = os.path.join(OUTDIR, f"{symbol.replace('/','')}.json")
    with open(output_file, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Saved {len(data)} candles for {symbol}")
    return data


if __name__ == "__main__":
    fetch_crypto_data()
