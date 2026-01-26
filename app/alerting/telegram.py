from __future__ import annotations
import os, asyncio
from typing import List
import httpx

TELEGRAM_API = "https://api.telegram.org"

async def send_message(text: str) -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    if not token or not chat_id:
        return
    url = f"{TELEGRAM_API}/bot{token}/sendMessage"
    async with httpx.AsyncClient() as client:
        await client.post(url, json={"chat_id": chat_id, "text": text, "parse_mode": "HTML"})

async def notify_rankings(rows: List[dict]) -> None:
    if not rows:
        return
    lines = ["<b>MemeCoin Scout — Top Picks</b>"]
    for r in rows[:10]:
        lines.append(f"{r['rank']}. <b>{r['symbol']}</b> ({r['chain']}) — score {r['score_total']}/100 — liq ${r['liquidity_usd']}, 1h vol ${r['vol1h']}")
    await send_message("\n".join(lines))
