"""
Logging utilities for Memecoin Scout
Handles console logging of detected tokens
"""

from datetime import datetime
from typing import Dict


def log_token(token: Dict) -> None:
    """
    Logs a single token to stdout in a clean, readable format.
    """

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    name = token.get("name", "UNKNOWN")
    symbol = token.get("symbol", "???")
    score = token.get("score", 0)

    liquidity = token.get("liquidity", {}).get("usd", 0)
    volume = token.get("volume", {}).get("h24", 0)
    holders = token.get("holders", "N/A")

    print(
        f"[{timestamp}] "
        f"{name} ({symbol}) | "
        f"Score: {score} | "
        f"Liquidity: ${liquidity:,.0f} | "
        f"24h Vol: ${volume:,.0f} | "
        f"Holders: {holders}"
    )
