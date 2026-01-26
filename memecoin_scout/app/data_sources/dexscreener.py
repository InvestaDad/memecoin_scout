import time
import asyncio
import httpx
from typing import List, Optional

from app.schemas import TokenInfo, LiquidityInfo, VolumeInfo, FiltersConfig


async def fetch_new_listings(
    chain: str = "solana",
    cfg: Optional[FiltersConfig] = None,
    max_age_minutes: int = 720
) -> List[TokenInfo]:
    """
    Fetch new token listings from DexScreener using search.
    Search endpoint returns up to 30 most relevant pairs per query.
    We search multiple queries to get more coverage.
    """
    
    # Use search to find new Solana tokens
    # Multiple queries to get better coverage (each returns ~30 pairs)
    search_queries = [
        "raydium",
        "orca", 
        "solana new",
        "pump.fun",
    ]
    
    all_pairs = []
    
    for query in search_queries:
        url = f"https://api.dexscreener.com/latest/dex/search?q={query}"
        
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                r = await client.get(url)
                r.raise_for_status()
                data = r.json()
                
                pairs = data.get("pairs", [])
                # Filter for Solana only
                solana_pairs = [p for p in pairs if p.get("chainId") == "solana"]
                all_pairs.extend(solana_pairs)
                
                print(f"[debug] Found {len(solana_pairs)} Solana pairs for query '{query}'")
                
        except httpx.HTTPStatusError as e:
            print(f"[error] DexScreener HTTP error for '{query}': {e.response.status_code}")
            continue
        except Exception as e:
            print(f"[error] DexScreener request failed for '{query}': {e}")
            continue
        
        # Small delay to avoid rate limiting
        await asyncio.sleep(0.5)
    
    # Remove duplicates based on pair address
    seen_addresses = set()
    unique_pairs = []
    for p in all_pairs:
        pair_address = p.get("pairAddress")
        if pair_address and pair_address not in seen_addresses:
            seen_addresses.add(pair_address)
            unique_pairs.append(p)
    
    print(f"[debug] Total unique Solana pairs found: {len(unique_pairs)}")

    if not unique_pairs:
        print("[warning] No pairs returned from DexScreener")
        return []

    now_ms = int(time.time() * 1000)
    tokens: List[TokenInfo] = []

    for p in unique_pairs:
        # Check pair creation time
        created_ms = p.get("pairCreatedAt")
        if not created_ms:
            continue

        # Calculate age in minutes
        age_m = int((now_ms - int(created_ms)) / 1000 / 60)
        if age_m > max_age_minutes:
            continue

        # Extract liquidity info
        liquidity_data = p.get("liquidity", {})
        liquidity = float(liquidity_data.get("usd", 0))
        
        if liquidity <= 0:
            continue

        # Extract volume and price
        volume_data = p.get("volume", {})
        volume_1h = float(volume_data.get("h1", 0))
        price_usd = float(p.get("priceUsd") or 0)
        fdv_usd = float(p.get("fdv") or 0)

        # Extract transaction data (5 minute window)
        txns_5m = p.get("txns", {}).get("m5", {})
        if not txns_5m:
            txns_5m = p.get("txns", {}).get("h1", {})  # Fallback to 1 hour
        
        trades_5m = int(txns_5m.get("buys", 0)) + int(txns_5m.get("sells", 0))

        # Extract base token info
        base = p.get("baseToken", {})
        symbol = base.get("symbol", "UNKNOWN")
        address = base.get("address", "")
        
        if not address:
            continue

        # Create token object
        token = TokenInfo(
            symbol=symbol,
            chain=chain,
            address=address,
            price_usd=price_usd,
            liquidity=LiquidityInfo(usd=liquidity),
            volume=VolumeInfo(usd_1h=volume_1h),
            age_minutes=age_m,
            fdv_usd=fdv_usd,
            dex_trades_5m=trades_5m
        )

        # Apply filters if provided
        if cfg:
            # Liquidity filter
            if not (cfg.min_liquidity_usd <= liquidity <= cfg.max_liquidity_usd):
                continue
            
            # Price filter
            if not (cfg.min_price_usd <= price_usd <= cfg.max_price_usd):
                continue

        tokens.append(token)

    print(f"[debug] {len(tokens)} live {chain} pairs accepted after filtering")
    
    # Sort by age (newest first)
    tokens.sort(key=lambda t: t.age_minutes)
    
    return tokens
