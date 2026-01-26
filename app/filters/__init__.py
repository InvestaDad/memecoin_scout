from typing import List
from app.schemas import TokenInfo, FiltersConfig

def filter_tokens(tokens: List[TokenInfo], cfg: FiltersConfig) -> List[TokenInfo]:
    """
    Filters TokenInfo objects based on FiltersConfig thresholds.
    Returns only tokens that pass all checks.
    """
    filtered = []

    for token in tokens:
        try:
            if token.price_usd < cfg.min_price_usd or token.price_usd > cfg.max_price_usd:
                continue
            if token.liquidity.usd < cfg.min_liquidity_usd or token.liquidity.usd > cfg.max_liquidity_usd:
                continue
            if token.holders.holder_count < cfg.min_holders:
                continue
            if token.age_minutes < 0 or token.age_minutes > cfg.max_age_minutes:
                continue
            filtered.append(token)
        except Exception:
            continue

    return filtered
