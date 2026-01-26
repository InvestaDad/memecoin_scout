"""
Momentum tracking logic
Detects sudden increases in volume and liquidity
"""

from typing import Dict
from datetime import datetime


def log_momentum(token: Dict) -> None:
    """
    Logs momentum-related information for a token.
    """

    name = token.get("name", "UNKNOWN")
    symbol = token.get("symbol", "???")
    score = token.get("score", 0)

    volume = token.get("volume", {}).get("h24", 0)
    liquidity = token.get("liquidity", {}).get("usd", 0)

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

    print(
        f"[MOMENTUM {timestamp}] "
        f"{name} ({symbol}) | "
        f"Score: {score} | "
        f"24h Vol: ${volume:,.0f} | "
        f"Liquidity: ${liquidity:,.0f}"
    )


def detect_momentum_spike(token: Dict) -> bool:
    """
    Simple heuristic to detect momentum spikes.
    Returns True if token shows strong early activity.
    """

    try:
        volume = float(token.get("volume", {}).get("h24", 0))
        liquidity = float(token.get("liquidity", {}).get("usd", 0))
        score = float(token.get("score", 0))

        # Very simple spike logic (safe + conservative)
        if volume > 50_000 and liquidity > 20_000 and score >= 50:
            return True

    except Exception:
        return False

    return False