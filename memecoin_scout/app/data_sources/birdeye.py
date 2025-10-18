import httpx
from ..schemas import HolderStats, CodeRisk

BIRDEYE_API = "https://public-api.birdeye.so/defi"

async def enrich_with_birdeye(token_address: str, api_key: str):
    """
    Fetch holders + security flags from Birdeye for a Solana token.
    """
    headers = {"x-api-key": api_key}

    async with httpx.AsyncClient(timeout=20) as client:
        # ✅ Get holder list
        try:
            h = await client.get(
                f"{BIRDEYE_API}/token/holder_list?address={token_address}&offset=0&limit=100",
                headers=headers,
            )
            h.raise_for_status()
            holders_data = h.json().get("data", [])
        except Exception as e:
            print(f"[birdeye] holder fetch failed for {token_address}: {e}")
            holders_data = []

        holder_count = len(holders_data)
        top1_pct, top5_pct = 0.0, 0.0
        if holders_data:
            balances = [float(x.get("amount", 0)) for x in holders_data]
            balances.sort(reverse=True)
            total = sum(balances) or 1
            top1_pct = balances[0] / total * 100
            top5_pct = sum(balances[:5]) / total * 100

        # ✅ Get security info (mint/freeze authority)
        try:
            s = await client.get(
                f"{BIRDEYE_API}/token/security?address={token_address}",
                headers=headers,
            )
            s.raise_for_status()
            sec = s.json().get("data", {})
        except Exception as e:
            print(f"[birdeye] security fetch failed for {token_address}: {e}")
            sec = {}

    return HolderStats(
        holder_count=holder_count,
        top1_pct=top1_pct,
        top5_pct=top5_pct,
    ), CodeRisk(
        sol_mint_authority_revoked=sec.get("mintAuthorityDisabled"),
        sol_freeze_authority_revoked=sec.get("freezeAuthorityDisabled"),
        owner_renounced_or_timelock=None,
        has_blacklist_or_whitelist=None,
    )
