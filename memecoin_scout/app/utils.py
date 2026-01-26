from __future__ import annotations
from typing import Any
from rich.table import Table
from rich import box

def _get(obj: Any, name: str, default=None):
    if obj is None:
        return default
    if isinstance(obj, dict):
        return obj.get(name, default)
    return getattr(obj, name, default)

def _fmt_usd(x) -> str:
    try:
        v = float(x or 0)
    except Exception:
        v = 0.0
    if v >= 1_000_000:
        return f"{v:,.0f}"
    return f"{v:,.0f}"

def _fmt_pct01(x) -> str:
    try:
        return f"{float(x or 0)*100:.0f}%"
    except Exception:
        return "0%"

def pretty_table(rows):
    table = Table(
        title="MemeCoin Scout — Ranked Survivors",
        box=box.SIMPLE_HEAVY
    )

    table.add_column("rank", justify="right", style="bold")
    table.add_column("symbol", style="bold")
    table.add_column("chain")
    table.add_column("score_total", justify="right")
    table.add_column("liq_score", justify="right")
    table.add_column("vol_score", justify="right")
    table.add_column("holders_score", justify="right")
    table.add_column("social_score", justify="right")
    table.add_column("code_score", justify="right")
    table.add_column("liquidity_usd", justify="right")
    table.add_column("vol1h", justify="right")
    table.add_column("trades5m", justify="right")
    table.add_column("holders", justify="right")
    table.add_column("lp_lock", justify="right")

    for i, r in enumerate(rows, start=1):
        sym = _get(r, "symbol", "?")
        chn = _get(r, "chain", "?")
        sc  = f"{float(_get(r, 'score_total', 0)):.1f}"

        liqs = f"{float(_get(r, 'liq_score', 0)):.2f}"
        vols = f"{float(_get(r, 'vol_score', 0)):.2f}"
        holds = f"{float(_get(r, 'holders_score', 0)):.2f}"
        socials = f"{float(_get(r, 'social_score', 0)):.2f}"
        codes = f"{float(_get(r, 'code_score', 0)):.2f}"

        liq_usd = _get(r, "liquidity_usd")
        if liq_usd is None:
            liq_obj = _get(r, "liquidity") or {}
            liq_usd = _get(liq_obj, "usd", 0)

        vol_obj = _get(r, "volume") or {}
        vol1h = _get(vol_obj, "volume_usd_1h", 0)
        trades5m = _get(vol_obj, "trades_5m", 0)

        h_obj = _get(r, "holders") or {}
        holders = _get(h_obj, "holder_count", 0) if not isinstance(h_obj, int) else h_obj

        l_obj = _get(r, "liquidity") or {}
        lp_lock = _get(l_obj, "lp_lock_ratio", 0)

        table.add_row(
            str(i), str(sym), str(chn), sc,
            liqs, vols, holds, socials, codes,
            _fmt_usd(liq_usd), _fmt_usd(vol1h),
            str(int(trades5m or 0)),
            str(int(holders or 0)),
            _fmt_pct01(lp_lock)
        )

    return table

