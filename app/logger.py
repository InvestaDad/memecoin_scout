import csv
import os
from datetime import datetime

LOG_FILE = os.path.join(os.path.dirname(__file__), "..", "token_logs.csv")

def log_token(token_data: dict):
    """Append a token's info to the CSV log."""
    file_exists = os.path.isfile(LOG_FILE)

    with open(LOG_FILE, mode="a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "timestamp",
            "symbol",
            "chain",
            "score",
            "liquidity",
            "volume",
            "holders",
            "lp_lock",
            "momentum_5m",
            "momentum_15m",
            "liquidity_stable",
            "link"
        ])

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            **token_data
        })

    print(f"[log] Saved token: {token_data.get('symbol')} ({token_data.get('score')}) → token_logs.csv")
