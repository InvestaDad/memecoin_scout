import httpx
import yaml
from ..schemas import HolderStats, CodeRisk

class BirdeyeSource:
    def __init__(self, config_path='config.yaml'):  # FIXED PATH
        with open(config_path) as f:
            cfg = yaml.safe_load(f)['data_sources']['birdeye']
        self.api_key = cfg['api_key']
        self.headers = {"x-api-key": self.api_key, "x-chain": "solana"}
    
    async def enrich_with_birdeye(self, token_address: str):
        async with httpx.AsyncClient(timeout=20) as client:
            holders_data = []
            try:
                h = await client.get(
                    f"https://public-api.birdeye.so/defi/token/holder_list?address={token_address}&limit=100",
                    headers=self.headers
                )
                holders_data = h.json().get("data", [])
            except:
                pass
            
            holder_count = len(holders_data)
            top1_pct = top5_pct = 0.0
            if holders_data:
                balances = [float(x.get("amount", 0)) for x in holders_data[:5]]
                total = sum(balances) or 1
                top1_pct = max(balances) / total * 100 if balances else 0
                top5_pct = total / total * 100
            
            sec = {"mintAuthorityDisabled": True}
            try:
                s = await client.get(
                    f"https://public-api.birdeye.so/defi/token/security?address={token_address}",
                    headers=self.headers
                )
                sec = s.json().get("data", {})
            except:
                pass
            
        return HolderStats(holder_count=holder_count, top1_pct=top1_pct, top5_pct=top5_pct), \
               CodeRisk(sol_mint_authority_revoked=sec.get("mintAuthorityDisabled"))
