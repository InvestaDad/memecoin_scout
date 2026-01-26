from typing import List
from .schemas import TokenInfo
from .config import FiltersConfig


def filter_tokens(tokens: List[TokenInfo], cfg: FiltersConfig) -> List[TokenInfo]:
    """
    Apply config.yaml filters to the list of tokens.
    Returns only the tokens that pass.
    Safely handles missing data fields.
    """
    passed = []
    
    print(f"\n[🔍 FILTER DEBUG] Checking {len(tokens)} tokens against filters...")
    
    for i, t in enumerate(tokens, 1):
        try:
            print(f"\n[Token {i}/{len(tokens)}] {t.symbol if hasattr(t, 'symbol') else 'Unknown'}")
            print(f"  Address: {t.address[:12] if hasattr(t, 'address') else 'N/A'}...")
            
            # Chain check
            if hasattr(t, 'chain') and t.chain not in cfg.chains:
                print(f"  ❌ Wrong chain: {t.chain}")
                continue
            
            # Liquidity check - REQUIRED
            liquidity_usd = 0
            if hasattr(t, 'liquidity') and hasattr(t.liquidity, 'usd'):
                liquidity_usd = t.liquidity.usd
            elif hasattr(t, 'liquidity_usd'):
                liquidity_usd = t.liquidity_usd
            
            print(f"  💧 Liquidity: ${liquidity_usd:,.0f} (min: ${cfg.min_liquidity_usd:,.0f})")
            if liquidity_usd < cfg.min_liquidity_usd:
                print(f"  ❌ Too low liquidity")
                continue
            
            # FDV check - OPTIONAL
            if hasattr(cfg, 'max_fdv_usd') and cfg.max_fdv_usd:
                if hasattr(t, 'fdv_usd') and t.fdv_usd and t.fdv_usd > cfg.max_fdv_usd:
                    print(f"  ❌ FDV too high: ${t.fdv_usd:,.0f} > ${cfg.max_fdv_usd:,.0f}")
                    continue
            
            # Holders check - OPTIONAL (often missing from DexScreener)
            if hasattr(cfg, 'min_holders') and cfg.min_holders > 0:
                holder_count = None
                if hasattr(t, 'holders') and t.holders and hasattr(t.holders, 'holder_count'):
                    holder_count = t.holders.holder_count
                elif hasattr(t, 'holder_count'):
                    holder_count = t.holder_count
                
                if holder_count is not None:
                    print(f"  👥 Holders: {holder_count} (min: {cfg.min_holders})")
                    if holder_count < cfg.min_holders:
                        print(f"  ❌ Not enough holders")
                        continue
                else:
                    print(f"  ⚠️  Holder data unavailable - SKIPPING check")
            
            # Age check - REQUIRED
            age_minutes = getattr(t, 'age_minutes', 0)
            print(f"  ⏰ Age: {age_minutes:.0f} min (range: {cfg.min_age_minutes}-{cfg.max_age_minutes})")
            if age_minutes < cfg.min_age_minutes:
                print(f"  ❌ Too young")
                continue
            if hasattr(cfg, 'max_age_minutes') and cfg.max_age_minutes and age_minutes > cfg.max_age_minutes:
                print(f"  ❌ Too old")
                continue
            
            # Tax checks - OPTIONAL
            if hasattr(cfg, 'max_buy_tax_bps') and cfg.max_buy_tax_bps:
                buy_tax = 0
                if hasattr(t, 'liquidity') and hasattr(t.liquidity, 'buy_tax_bps') and t.liquidity.buy_tax_bps:
                    buy_tax = t.liquidity.buy_tax_bps
                if buy_tax > cfg.max_buy_tax_bps:
                    print(f"  ❌ Buy tax too high: {buy_tax} bps")
                    continue
            
            if hasattr(cfg, 'max_sell_tax_bps') and cfg.max_sell_tax_bps:
                sell_tax = 0
                if hasattr(t, 'liquidity') and hasattr(t.liquidity, 'sell_tax_bps') and t.liquidity.sell_tax_bps:
                    sell_tax = t.liquidity.sell_tax_bps
                if sell_tax > cfg.max_sell_tax_bps:
                    print(f"  ❌ Sell tax too high: {sell_tax} bps")
                    continue
            
            # Holder concentration - OPTIONAL
            if hasattr(cfg, 'max_top1_holder_pct') and cfg.max_top1_holder_pct:
                if hasattr(t, 'holders') and t.holders and hasattr(t.holders, 'top1_pct') and t.holders.top1_pct:
                    if t.holders.top1_pct > cfg.max_top1_holder_pct:
                        print(f"  ❌ Top holder owns {t.holders.top1_pct}% (max: {cfg.max_top1_holder_pct}%)")
                        continue
            
            # Mint authority check - OPTIONAL
            if hasattr(cfg, 'require_mint_authority_revoked') and cfg.require_mint_authority_revoked:
                mint_revoked = False
                if hasattr(t, 'code_risk') and t.code_risk and hasattr(t.code_risk, 'sol_mint_authority_revoked'):
                    mint_revoked = t.code_risk.sol_mint_authority_revoked
                
                if not mint_revoked:
                    print(f"  ❌ Mint authority not revoked")
                    continue
            
            # LP lock check - OPTIONAL
            if hasattr(cfg, 'min_lp_lock_ratio') and cfg.min_lp_lock_ratio and cfg.min_lp_lock_ratio > 0:
                lp_lock = 0
                if hasattr(t, 'liquidity') and hasattr(t.liquidity, 'lp_lock_ratio') and t.liquidity.lp_lock_ratio:
                    lp_lock = t.liquidity.lp_lock_ratio
                if lp_lock < cfg.min_lp_lock_ratio:
                    print(f"  ❌ LP lock too low: {lp_lock:.0%} < {cfg.min_lp_lock_ratio:.0%}")
                    continue
            
            # Volume/trades checks - OPTIONAL
            if hasattr(cfg, 'min_dex_trades_5m') and cfg.min_dex_trades_5m > 0:
                trades = 0
                if hasattr(t, 'volume') and hasattr(t.volume, 'trades_5m') and t.volume.trades_5m:
                    trades = t.volume.trades_5m
                elif hasattr(t, 'trades_5m'):
                    trades = t.trades_5m
                
                if trades < cfg.min_dex_trades_5m:
                    print(f"  ❌ Not enough trades: {trades} < {cfg.min_dex_trades_5m}")
                    continue
            
            if hasattr(cfg, 'min_volume_usd_1h') and cfg.min_volume_usd_1h > 0:
                volume = 0
                if hasattr(t, 'volume') and hasattr(t.volume, 'volume_usd_1h') and t.volume.volume_usd_1h:
                    volume = t.volume.volume_usd_1h
                elif hasattr(t, 'volume_1h_usd'):
                    volume = t.volume_1h_usd
                
                if volume < cfg.min_volume_usd_1h:
                    print(f"  ❌ Low volume: ${volume:,.0f} < ${cfg.min_volume_usd_1h:,.0f}")
                    continue
            
            # ✅ PASSED ALL FILTERS!
            print(f"  ✅ PASSED all filters!")
            passed.append(t)
            
        except Exception as e:
            print(f"  ⚠️  Filter error: {e}")
            continue
    
    print(f"\n[🎯 RESULT] {len(passed)}/{len(tokens)} tokens passed filters\n")
    return passed
