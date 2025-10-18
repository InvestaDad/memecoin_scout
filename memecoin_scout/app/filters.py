from typing import List
from .schemas import TokenInfo
from .config import FiltersConfig

def filter_tokens(tokens: List[TokenInfo], cfg: FiltersConfig) -> List[TokenInfo]:
    """
    Apply config.yaml filters to the list of tokens.
    Returns only the tokens that pass.
    """
    passed = []
    for t in tokens:
        try:
            if t.chain not in cfg.chains:
                continue
            if t.liquidity.usd < cfg.min_liquidity_usd:
                continue
            if t.fdv_usd and t.fdv_usd > cfg.max_fdv_usd:
                continue
            if t.holders and t.holders.holder_count < cfg.min_holders:
                continue
            if t.age_minutes < cfg.min_age_minutes:
                continue
            if cfg.max_age_minutes and t.age_minutes > cfg.max_age_minutes:
                continue
            if t.liquidity.buy_tax_bps > cfg.max_buy_tax_bps:
                continue
            if t.liquidity.sell_tax_bps > cfg.max_sell_tax_bps:
                continue
            if t.holders and t.holders.top1_pct and t.holders.top1_pct > cfg.max_top1_holder_pct:
                continue
            if t.holders and t.holders.top5_pct and t.holders.top5_pct > cfg.max_top5_holder_pct:
                continue
            if cfg.require_mint_authority_revoked and not t.code_risk.sol_mint_authority_revoked:
                continue
            if cfg.min_lp_lock_ratio and t.liquidity.lp_lock_ratio < cfg.min_lp_lock_ratio:
                continue
            if t.volume.trades_5m < cfg.min_dex_trades_5m:
                continue
            if t.volume.volume_usd_1h < cfg.min_volume_usd_1h:
                continue

            passed.append(t)
        except Exception as e:
            print("[filter error]", e)
            continue

    return passed
