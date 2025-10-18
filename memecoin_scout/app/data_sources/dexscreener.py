from __future__ import annotations
import os
import time
import asyncio
import httpx
from typing import List

from ..schemas import TokenInfo, LiquidityInfo, HolderStats, VolumeInfo, SocialInfo, CodeRisk
from .birdeye import enrich_with_birdeye

# DexScreener API URL
SEARCH_URL = "https://api.dexscreener.com/latest/dex/search"

# Birdeye API Key from environment variable
BIRDEYE_KEY = os.getenv("BIRDEYE_API_KEY")

async def fetch_new_listings(max_age_minutes: int = 60, limit: int = 50) -> List[TokenInfo]:
    """
    Fetch the newest Solana tokens from DexScreener and enrich them with Birdeye data.
    """
    params = {"q": "raydium solana"}
    tokens: List[TokenInfo] = []

    async with httpx.AsyncClient(timeout=20) as client:
        r = await client.get(SEARCH_URL, params=params)
        r.raise_for_status()
        data = r.json()

    print("[debug] DexScreener response keys:", data.keys())
    print("[debug] number of pairs:", len(data.get("pairs", [])))
    for pair in data.get("pairs", [])[:5]:
        base = (pair.get("baseToken") or {}).get("symbol")
        chain = pair.get("chainId")
        print("   -", base, "on", chain)

    now_ms = int(time.time() * 1000)
    for p in data.get("pairs", [])[:limit]:
        if p.get("chainId") != "solana":
            continue

        created_ms = p.get("pairCreatedAt")
        age_minutes = int((now_ms - created_ms) / 60000) if created_ms else 0
        if created_ms and age_minutes > max_age_minutes:
            continue

        txns = p.get("txns") or {}
        m5 = txns.get("m5") or {}
        volume = p.get("volume") or {}
        info = p.get("info") or {}
        socials = info.get("socials") or []
        tw_handle = next((s.get("handle") for s in socials if s.get("platform") in ("twitter", "x")), None)

        token = TokenInfo(
            name=(p.get("baseToken") or {}).get("name") or "?",
            symbol=(p.get("baseToken") or {}).get("symbol") or "?",
            chain="solana",
            address=(p.get("baseToken") or {}).get("address") or "",
            pair_address=p.get("pairAddress"),
            age_minutes=age_minutes,
            fdv_usd=p.get("fdv"),
            liquidity=LiquidityInfo(
                usd=((p.get("liquidity") or {}).get("usd") or 0),
                lp_lock_ratio=0.0,
                buy_tax_bps=0,
                sell_tax_bps=0,
            ),
            holders=HolderStats(holder_count=0, top1_pct=0.0, top5_pct=0.0),
            volume=VolumeInfo(
                volume_usd_5m=0.0,
                volume_usd_1h=(volume.get("h1") or 0),
                trades_5m=int((m5.get("buys") or 0) + (m5.get("sells") or 0)),
                buyers_5m=int(m5.get("buys") or 0),
                sellers_5m=int(m5.get("sells") or 0),
            ),
            social=SocialInfo(twitter_handle=tw_handle),
            code_risk=CodeRisk(
                sol_mint_authority_revoked=None,
                sol_freeze_authority_revoked=None,
                owner_renounced_or_timelock=None,
                has_blacklist_or_whitelist=None,
            ),
            honeypot_flag=False,
        )

        # 🔥 Enrich with Birdeye (holders + mint/freeze authority)
        if BIRDEYE_KEY and token.address:
            try:
                holders, risk = await enrich_with_birdeye(token.address, BIRDEYE_KEY)
                token.holders = holders
                token.code_risk = risk
                await asyncio.sleep(1.0)  # ⏳ stay under 60 requests/min (safe)
            except httpx.HTTPStatusError as e:
                print(f"[birdeye] HTTP error for {token.symbol}: {e.response.status_code}")
            except Exception as e:
                print(f"[birdeye] failed for {token.symbol}: {e}")

        tokens.append(token)

    return tokens


def normalize_from_dict(d: dict) -> TokenInfo:
    """
    Rebuild a TokenInfo object from a dictionary (used for demo/testing).
    """
    return TokenInfo(
        name=d.get("name", "?"),
        symbol=d.get("symbol", "?"),
        chain=d.get("chain", "solana"),
        address=d.get("address", ""),
        pair_address=d.get("pair_address"),
        age_minutes=int(d.get("age_minutes", 0)),
        fdv_usd=d.get("fdv_usd"),
        liquidity=LiquidityInfo(**d.get("liquidity", {})),
        holders=HolderStats(**d.get("holders", {})),
        volume=VolumeInfo(**d.get("volume", {})),
        social=SocialInfo(**d.get("social", {})),
        code_risk=CodeRisk(**d.get("code_risk", {})),
        honeypot_flag=d.get("honeypot_flag", False),
    )
