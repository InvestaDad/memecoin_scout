from pydantic import BaseModel
from typing import List, Optional

class FiltersConfig(BaseModel):
    chains: List[str]
    min_liquidity_usd: float
    max_fdv_usd: float
    min_holders: int
    min_age_minutes: int
    max_age_minutes: Optional[int] = None
    max_buy_tax_bps: int
    max_sell_tax_bps: int
    max_top1_holder_pct: float
    max_top5_holder_pct: float
    require_contract_verified: bool = False
    require_owner_renounced_or_timelock: bool = False
    require_mint_authority_revoked: bool = False
    min_lp_lock_ratio: float = 0.0
    min_dex_trades_5m: int = 0
    min_volume_usd_1h: float = 0.0
