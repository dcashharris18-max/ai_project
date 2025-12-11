"""Trading service using CCXT (wrapper)

This module provides a small wrapper around CCXT for market data
and optional order placement. For production you must securely
manage API keys and implement error handling, rate-limits, and
logging.
"""
from typing import Optional
import ccxt
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "..", "..", ".env"))

CCXT_EXCHANGE = os.getenv("CCXT_EXCHANGE", "binance")
CCXT_API_KEY = os.getenv("CCXT_API_KEY")
CCXT_SECRET = os.getenv("CCXT_SECRET")


def get_exchange():
    exchange_cls = getattr(ccxt, CCXT_EXCHANGE)
    if CCXT_API_KEY and CCXT_SECRET:
        return exchange_cls({"apiKey": CCXT_API_KEY, "secret": CCXT_SECRET})
    return exchange_cls()


def fetch_ohlcv(symbol: str = "BTC/USDT", timeframe: str = "1h", limit: int = 100):
    ex = get_exchange()
    return ex.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)


def fetch_ticker(symbol: str = "BTC/USDT"):
    ex = get_exchange()
    return ex.fetch_ticker(symbol)


def place_market_order(
    symbol: str, side: str, amount: float, price: Optional[float] = None
):
    """Place a market order. Requires API keys configured."""
    ex = get_exchange()
    if not CCXT_API_KEY or not CCXT_SECRET:
        raise RuntimeError("Exchange API keys not configured")
    # side = 'buy' or 'sell'
    return ex.create_market_order(symbol, side, amount)
