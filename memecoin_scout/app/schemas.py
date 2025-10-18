from pydantic import BaseModel
from typing import Optional


class LiquidityInfo(BaseModel):
    usd: float = 0.0
    lp_lock_ratio: float = 0.0
    buy_tax_bps: Optional[int] = 0
    sell_tax_bps: Optional[int] = 0


class HolderStats(BaseModel):
    holder_count: int = 0
    top1_pct: float = 0.0
    top5_pct: float = 0.0


class VolumeInfo(BaseModel):
    volume_usd_5m: float = 0.0
    volume_usd_1h: float = 0.0
    trades_5m: int = 0
    buyers_5m: int = 0
    sellers_5m: int = 0


class SocialInfo(BaseModel):
    twitter_handle: Optional[str] = None
    telegram: Optional[str] = None
    website: Optional[str] = None


class CodeRisk(BaseModel):
    sol_mint_authority_revoked: Optional[bool] = None
    sol_freeze_authority_revoked: Optional[bool] = None
    owner_renounced_or_timelock: Optional[bool] = None
    has_blacklist_or_whitelist: Optional[bool] = None


class TokenInfo(BaseModel):
    name: str
    symbol: str
    chain: str
    address: str
    pair_address: Optional[str] = None
    age_minutes: Optional[int] = 0
    fdv_usd: Optional[float] = None
    liquidity: LiquidityInfo
    holders: HolderStats
    volume: VolumeInfo
    social: Optional[SocialInfo] = None
    code_risk: Optional[CodeRisk] = None
    honeypot_flag: Optional[bool] = False
    score_total: Optional[float] = None   # ✅ Added for scoring support
