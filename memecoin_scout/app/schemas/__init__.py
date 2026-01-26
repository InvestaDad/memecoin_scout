from pydantic import BaseModel
from typing import List, Optional


# -------------------------------
# Basic Data Models
# -------------------------------
class LiquidityInfo(BaseModel):
    usd: float = 0.0
    lp_lock_ratio: float = 0.0


class VolumeInfo(BaseModel):
    usd_1h: float = 0.0
    usd_24h: float = 0.0


class HolderStats(BaseModel):
    holder_count: int = 0
    top1_pct: float = 0.0
    top5_pct: float = 0.0


class SocialInfo(BaseModel):
    telegram_followers: int = 0
    twitter_followers: int = 0
    sentiment_score: float = 0.0


class CodeRisk(BaseModel):
    verified: bool = False
    mint_revoked: bool = True
    renounced: bool = True


# -------------------------------
# Main Token Info
# -------------------------------
class TokenInfo(BaseModel):
    symbol: str
    chain: str
    address: Optional[str] = None
    price_usd: float = 0.0
    liquidity: LiquidityInfo = LiquidityInfo()
    volume: VolumeInfo = VolumeInfo()
    holders: HolderStats = HolderStats()
    socials: SocialInfo = SocialInfo()
    code_risk: CodeRisk = CodeRisk()
    age_minutes: int = 0
    fdv_usd: Optional[float] = None
    buy_tax_bps: Optional[int] = None
    sell_tax_bps: Optional[int] = None
    dex_trades_5m: Optional[int] = None
    score_total: Optional[float] = None


# -------------------------------
# Easiest Mode FiltersConfig
# -------------------------------
class FiltersConfig(BaseModel):
    chains: List[str] = ["solana"]

    # Price filters
    min_price_usd: float = 0.000001
    max_price_usd: float = 1.0

    # Liquidity filters
    min_liquidity_usd: float = 1000
    max_liquidity_usd: float = 50_000

    # Market cap / FDV
    max_fdv_usd: float = 50_000_000

    # Holder distribution
    min_holders: int = 10
    max_top1_holder_pct: float = 100
    max_top5_holder_pct: float = 100

    # Age
    min_age_minutes: int = 0
    max_age_minutes: int = 2_880  # last 2 days

    # Taxes
    max_buy_tax_bps: int = 10_000
    max_sell_tax_bps: int = 10_000

    # Contract / risk
    require_contract_verified: bool = False
    require_owner_renounced_or_timelock: bool = False
    require_mint_authority_revoked: bool = False

    # Liquidity safety
    min_lp_lock_ratio: float = 0.0

    # Activity
    min_dex_trades_5m: int = 0
    min_volume_usd_1h: float = 0


# -------------------------------
# Optional: scoring weights
# -------------------------------
class ScoreWeights(BaseModel):
    liquidity: float = 0.25
    volume_momentum: float = 0.25
    buyers_sellers_trend: float = 0.15
    holder_distribution: float = 0.15
    social_trend: float = 0.15
    code_risk: float = 0.05
