from typing import List
from .schemas import TokenInfo
from .config import FiltersConfig

def score_tokens(tokens: List[TokenInfo], cfg: FiltersConfig) -> List[TokenInfo]:
    """
    Assign a composite score to tokens based on weights from config.yaml.
    """
    results = []
    for t in tokens:
        try:
            liquidity_score = min(1.0, t.liquidity.usd / max(cfg.min_liquidity_usd, 1))
            volume_score = min(1.0, t.volume.volume_usd_1h / max(cfg.min_volume_usd_1h, 1))
            holder_score = min(1.0, (t.holders.holder_count or 0) / max(cfg.min_holders, 1))
            trade_score = min(1.0, (t.volume.trades_5m or 0) / max(cfg.min_dex_trades_5m, 1))

            # Simple weighted score (you can extend with config weights)
            total_score = (
                0.3 * liquidity_score +
                0.3 * volume_score +
                0.2 * holder_score +
                0.2 * trade_score
            )

            t.score_total = round(total_score * 100, 2)  # out of 100
            results.append(t)

        except Exception as e:
            print("[scoring error]", e)
            continue

    # Sort highest score first
    results.sort(key=lambda x: getattr(x, "score_total", 0), reverse=True)
    return results

def score_tokens(tokens, cfg):
    scored = []
    for t in tokens:
        try:
            score = 0
            # Example scoring logic
            if t.liquidity.usd > cfg.min_liquidity_usd:
                score += 20
            if t.volume.volume_usd_1h > cfg.min_volume_usd_1h:
                score += 20
            if t.holders.holder_count > cfg.min_holders:
                score += 20
            if t.liquidity.lp_lock_ratio > cfg.min_lp_lock_ratio:
                score += 20
            if not t.honeypot_flag:
                score += 20

            t.score_total = score  # ✅ add the field dynamically
            scored.append(t)

        except Exception as e:
            print(f"[scoring error] {e}")

    return scored


