import asyncio
import time
import yaml
from app.filters import filter_tokens
from app.scorer import score_tokens
from app.data_sources.dexscreener import fetch_new_listings
from app.config import FiltersConfig

async def main_loop(cfg):
    while True:
        print(f"\n[{time.strftime('%H:%M:%S')}] fetching new tokens…")
        try:
            tokens = await fetch_new_listings(
                max_age_minutes=cfg.max_age_minutes,
                limit=20
            )
            filtered = filter_tokens(tokens, cfg)
            scored = score_tokens(filtered, cfg)

            if scored:
                print(f"[+] Found {len(scored)} candidates\n")
                for t in scored:
                    print(
                        f"  - {t.symbol} | liq ${t.liquidity.usd} | "
                        f"holders {t.holders.holder_count} | "
                        f"LP lock {t.liquidity.lp_lock_ratio*100:.1f}% | "
                        f"age {t.age_minutes}m"
                    )
            else:
                print("[-] No tokens passed filters this round")

        except Exception as e:
            print("[error]", e)

        await asyncio.sleep(180)  # wait 3 minutes and try again

if __name__ == "__main__":
    with open("config.yaml") as f:
        cfg_raw = yaml.safe_load(f)
    cfg = FiltersConfig(**cfg_raw["global"])

    asyncio.run(main_loop(cfg))
