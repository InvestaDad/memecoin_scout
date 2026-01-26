# app/momentum_tracker.py
# Tracks token price and liquidity changes to detect sudden "degen" momentum

import os
import csv
from datetime import datetime, timezone

MOMENTUM_FILE = os.path.join(os.path.dirname(__file__), "data", "momentum.csv")

os.makedirs(os.path.dirname(MOMENTUM_FILE), exist_ok=True)

def log_momentum(address, symbol, price_usd, liquidity_usd):
    """Log a snapshot of price & liquidity for a token."""
    file_exists = os.path.isfile(MOMENTUM_FILE)

    with open(MOMENTUM_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "ts",
            "address",
            "symbol",
            "price_usd",
            "liquidity_usd"
        ])

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "ts": int(datetime.now(timezone.utc).timestamp()),
            "address": address,
            "symbol": symbol,
            "price_usd": price_usd,
            "liquidity_usd": liquidity_usd,
        })

def detect_momentum_spike(symbol, df, lookback=5):
    """
    Detect strong price spikes over the last few records (5 by default).
    Returns (True, pct_change) if spike > +30%.
    """
    if df.empty or len(df) < lookback:
        return False, 0

    recent = df.tail(lookback)
    first, last = recent.iloc[0]["price_usd"], recent.iloc[-1]["price_usd"]
    if first <= 0:
        return False, 0

    pct = ((last - first) / first) * 100
    return pct > 30, round(pct, 1)
