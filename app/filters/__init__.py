from typing import List
from ..schemas import TokenInfo, FiltersConfig


def filter_tokens(tokens: List[TokenInfo], cfg: FiltersConfig) -> List[TokenInfo]:
    """
    Filters TokenInfo objects based on FiltersConfig thresholds.
    Returns only tokens that pass all checks.
    Safely handles missing data fields.
    """
    filtered = []
    
    print(f"\n[FILTER] Checking {len(tokens)} tokens against filters...")

    for i, token in enumerate(tokens, 1):
        try:
            print(f"\n[Token {i}/{len(tokens)}] {getattr(token, 'symbol', 'Unknown')}")
            print(f"  Address: {token.address[:12] if hasattr(token, 'address') else 'N/A'}...")
            
            # Price check
            price = getattr(token, 'price_usd', 0)
            if price < cfg.min_price_usd or price > cfg.max_price_usd:
                print(f"  [X] Price ${price:.8f} out of range (${cfg.min_price_usd:.8f} - ${cfg.max_price_usd:.2f})")
                continue
            
            # Liquidity check
            liquidity = 0
            if hasattr(token, 'liquidity') and hasattr(token.liquidity, 'usd'):
                liquidity = token.liquidity.usd
            elif hasattr(token, 'liquidity_usd'):
                liquidity = token.liquidity_usd
            
            if liquidity < cfg.min_liquidity_usd or liquidity > cfg.max_liquidity_usd:
                print(f"  [X] Liquidity ${liquidity:,.0f} out of range (${cfg.min_liquidity_usd:,.0f} - ${cfg.max_liquidity_usd:,.0f})")
                continue
            
            # Holders check - OPTIONAL (DexScreener often doesn't have this)
            if hasattr(cfg, 'min_holders') and cfg.min_holders > 0:
                holder_count = None
                
                if hasattr(token, 'holders') and token.holders and hasattr(token.holders, 'holder_count'):
                    holder_count = token.holders.holder_count
                elif hasattr(token, 'holder_count'):
                    holder_count = token.holder_count
                
                if holder_count is not None:
                    if holder_count < cfg.min_holders:
                        print(f"  [X] Holders {holder_count} < minimum {cfg.min_holders}")
                        continue
                else:
                    print(f"  [!] Holder data unavailable - skipping holder check")
            
            # Age check
            age_minutes = getattr(token, 'age_minutes', 0)
            age_days = age_minutes / 1440
            max_age_days = cfg.max_age_minutes / 1440 if hasattr(cfg, 'max_age_minutes') else 0
            
            if age_minutes < 0:
                print(f"  [X] Invalid age: {age_minutes}")
                continue
            
            if hasattr(cfg, 'max_age_minutes') and age_minutes > cfg.max_age_minutes:
                print(f"  [X] Age {age_days:.1f} days > max {max_age_days:.0f} days")
                continue
            
            # Volume check - OPTIONAL
            if hasattr(cfg, 'min_volume_usd_1h') and cfg.min_volume_usd_1h > 0:
                volume = 0
                if hasattr(token, 'volume') and hasattr(token.volume, 'usd_1h'):
                    volume = token.volume.usd_1h
                elif hasattr(token, 'volume_1h_usd'):
                    volume = token.volume_1h_usd
                
                if volume < cfg.min_volume_usd_1h:
                    print(f"  [X] Volume ${volume:,.0f} < minimum ${cfg.min_volume_usd_1h:,.0f}")
                    continue
            
            # PASSED
            print(f"  [OK] PASSED - Price: ${price:.8f}, Liq: ${liquidity:,.0f}, Age: {age_days:.1f}d")
            filtered.append(token)
            
        except Exception as e:
            print(f"  [!] Filter error: {e}")
            continue

    print(f"\n[RESULT] {len(filtered)}/{len(tokens)} tokens passed filters\n")
    return filtered
