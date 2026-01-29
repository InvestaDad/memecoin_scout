from dotenv import load_dotenv
load_dotenv()

import asyncio
import yaml
import re
from pathlib import Path
from datetime import datetime, timezone
from app.data_sources.dexscreener import fetch_new_listings
from app.schemas import TokenInfo, LiquidityInfo, VolumeInfo, FiltersConfig
from app.filters import filter_tokens
from app.scorer import score_tokens
from app.alerting.telegram_alert import send_telegram_alert
from app.logger import log_token
from app.momentum_tracker import detect_momentum_spike
from app.coingecko_client import CoinGeckoClient
from app.ethereum_scanner import scan_ethereum_contract



# Keep track of tokens we've already processed
processed_addresses = set()



def load_config_with_env(config_path='config.yaml'):
    """
    Load config.yaml and replace ${VARIABLE} with environment variables
    """
    with open(config_path, 'r') as f:
        config_text = f.read()
        
        # Replace ${VARIABLE} with actual environment values
        def replace_env_var(match):
            var_name = match.group(1)
            env_value = os.getenv(var_name)
            if env_value:
                return env_value
            else:
                print(f"[WARNING] Environment variable {var_name} not found in .env")
                return match.group(0)
        
        config_text = re.sub(r'\$\{(\w+)\}', replace_env_var, config_text)
        return yaml.safe_load(config_text)



async def process_token(token: TokenInfo, cfg: FiltersConfig, coingecko: CoinGeckoClient):
    """
    Process a single token:
    - Apply filters
    - Fetch CoinGecko data
    - Score it
    - Detect momentum
    - Log
    - Send Telegram alerts
    """
    if not filter_tokens([token], cfg):
        return None


    # Fetch additional data from CoinGecko
    try:
        cg_data = await coingecko.get_token_data(token.address)
        
        if cg_data:
            token.coingecko_score = cg_data.get('coingecko_score')
            token.community_score = cg_data.get('community_score')
            token.liquidity_score = cg_data.get('liquidity_score')
            token.twitter_followers = cg_data.get('twitter_followers')
            token.telegram_users = cg_data.get('telegram_users')
            
            if token.community_score:
                print(f"  [CoinGecko] Enhanced {token.symbol} - Community: {token.community_score:.1f}/100")
            else:
                print(f"  [CoinGecko] Found {token.symbol} data")
    except Exception as e:
        print(f"  [CoinGecko] No data for {token.symbol}")


    score_tokens(token)
    detect_momentum_spike(token)
    log_token(token)
    await send_telegram_alert(token)


    return token



async def process_ethereum_token(address: str):
    """
    Process an Ethereum contract address
    Uses the ethereum_scanner module
    """
    try:
        print(f"\n[ETHEREUM SCAN] Analyzing contract: {address}")
        result = scan_ethereum_contract(address)
        
        if result.get('error'):
            print(f"  ❌ Error: {result['error']}")
            return None
        
        # Display results
        print(f"\n{'='*70}")
        print(f"  Chain: {result['chain'].upper()}")
        print(f"  Address: {result['address']}")
        print(f"  Is Contract: {result['is_contract']}")
        print(f"  Risk Score: {result['risk_score']}/100")
        print(f"  Verdict: {result['verdict']}")
        print(f"{'='*70}")
        
        if result.get('flags'):
            print(f"\n  Security Flags:")
            for flag in result['flags']:
                print(f"    • {flag}")
        
        if result.get('recommendations'):
            print(f"\n  Recommendations:")
            for rec in result['recommendations']:
                print(f"    • {rec}")
        
        print(f"\n{'='*70}\n")
        
        return result
        
    except Exception as e:
        print(f"  [ERROR] Ethereum scan failed: {e}")
        return None



async def main(cfg: FiltersConfig):
    """Main scanning loop"""
    print("\n" + "="*70)
    print("MEMECOIN SCOUT - HIDDEN GEM SCANNER")
    print("="*70)
    print(f"[{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}] Starting...")
    print(f"Filters: Liquidity ${cfg.min_liquidity_usd:,.0f} - ${cfg.max_liquidity_usd:,.0f}")
    print(f"Price: ${cfg.min_price_usd} - ${cfg.max_price_usd}")
    print(f"Max Age: {cfg.max_age_minutes} minutes")
    print(f"API Keys: Loaded from .env")
    print("="*70 + "\n")
    
    # Initialize CoinGecko client
    coingecko = CoinGeckoClient()
    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] CoinGecko client initialized\n")
    
    scan_count = 0
    
    while True:
        try:
            scan_count += 1
            print(f"\n{'-'*70}")
            print(f"[SCAN #{scan_count}] {datetime.now(timezone.utc).strftime('%H:%M:%S UTC')}")
            print(f"{'-'*70}")
            
            new_tokens = await fetch_new_listings(chain='solana', cfg=cfg, max_age_minutes=cfg.max_age_minutes)
            new_tokens = [t for t in new_tokens if t.address not in processed_addresses]


            if not new_tokens:
                print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] No new hidden gems found this scan")
            else:
                print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] Processing {len(new_tokens)} new tokens...\n")
                
                tasks = [process_token(t, cfg, coingecko) for t in new_tokens]
                results = await asyncio.gather(*tasks)
                processed_tokens = [t for t in results if t is not None]


                if processed_tokens:
                    processed_tokens.sort(
                        key=lambda x: x.score_total if x.score_total is not None else x.liquidity.usd,
                        reverse=True
                    )


                    print(f"\nTOP HIDDEN GEMS (Scan #{scan_count}):")
                    print("-"*70)
                    for i, t in enumerate(processed_tokens[:5], 1):
                        score_display = f"{t.score_total:.2f}" if t.score_total else "N/A"
                        cg_display = f"CG:{t.coingecko_score:.0f}" if t.coingecko_score else ""
                        print(
                            f"  {i}. ${t.symbol} | Price: ${t.price_usd:.8f} | "
                            f"Liq: ${t.liquidity.usd:,.0f} | Score: {score_display} {cg_display} | Age: {t.age_minutes}m"
                        )


                    for t in processed_tokens:
                        processed_addresses.add(t.address)
                else:
                    print(f"[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] No tokens passed all filters")


            next_scan = datetime.now(timezone.utc)
            print(f"\n[{datetime.now(timezone.utc).strftime('%H:%M:%S')}] Next scan in 60 seconds")
            
            await asyncio.sleep(60)


        except KeyboardInterrupt:
            print("\n\n[INFO] Scanner stopped by user")
            break
        except Exception as e:
            print(f"[ERROR] Main loop exception: {e}")
            print(f"[INFO] Retrying in 30 seconds...")
            await asyncio.sleep(30)



if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Memecoin Scout - Hidden Gem Scanner")
    parser.add_argument("--live", action="store_true", help="Run in live mode")
    parser.add_argument("--config", type=str, default="../config.yaml", help="Path to config file")
    parser.add_argument("--eth-scan", type=str, help="Scan a single Ethereum contract address")
    args = parser.parse_args()
    
    # Handle Ethereum contract scanning mode
    if args.eth_scan:
        print("\n" + "="*70)
        print("ETHEREUM CONTRACT SECURITY SCANNER")
        print("="*70)
        
        result = scan_ethereum_contract(args.eth_scan)
        
        if result.get('error'):
            print(f"\n❌ Error: {result['error']}")
            exit(1)
        else:
            print(f"\n✅ Scan Complete:")
            print(f"  Chain: {result['chain'].upper()}")
            print(f"  Address: {result['address']}")
            print(f"  Is Contract: {result['is_contract']}")
            print(f"  Risk Score: {result['risk_score']}/100")
            print(f"  Verdict: {result['verdict']}")
            
            if result.get('flags'):
                print(f"\n  Security Flags:")
                for flag in result['flags']:
                    print(f"    • {flag}")
            
            if result.get('recommendations'):
                print(f"\n  Recommendations:")
                for rec in result['recommendations']:
                    print(f"    • {rec}")
            
            if result.get('checks', {}).get('goplus_data'):
                gp = result['checks']['goplus_data']
                print(f"\n  GoPlus Security Data:")
                print(f"    • Honeypot: {gp.get('is_honeypot', False)}")
                print(f"    • Buy Tax: {gp.get('buy_tax', 0)*100:.1f}%")
                print(f"    • Sell Tax: {gp.get('sell_tax', 0)*100:.1f}%")
                print(f"    • Holder Count: {gp.get('holder_count', 0)}")
                print(f"    • Mintable: {gp.get('is_mintable', False)}")
                print(f"    • Proxy: {gp.get('is_proxy', False)}")
            
            print(f"\n{'='*70}\n")
            exit(0)
    
    # Continue with normal Solana scanning mode
    try:
        # Load config with environment variable support
        config_path = Path(args.config)
        config_data = load_config_with_env(config_path)
        
        filters_section = config_data.get('filters', {})
        global_section = config_data.get('global', {})
        
        cfg = FiltersConfig(
            min_liquidity_usd=filters_section.get('min_liquidity_usd', global_section.get('min_liquidity_usd', 3000)),
            max_liquidity_usd=filters_section.get('max_liquidity_usd', 750000),
            min_price_usd=filters_section.get('min_price_usd', 0.0000001),
            max_price_usd=filters_section.get('max_price_usd', 0.10),
            min_holders=global_section.get('min_holders', 50),
            max_age_minutes=global_section.get('max_age_minutes', 720),
            min_dex_trades_5m=global_section.get('min_dex_trades_5m', 5),
            min_volume_usd_1h=global_section.get('min_volume_usd_1h', 500),
            require_contract_verified=global_section.get('require_contract_verified', False),
            require_owner_renounced_or_timelock=global_section.get('require_owner_renounced_or_timelock', False),
            require_mint_authority_revoked=global_section.get('require_mint_authority_revoked', True),
        )
        
        print(f"[SUCCESS] Loaded config from {args.config}")
        print(f"[SUCCESS] Environment variables loaded from .env\n")
        
    except Exception as e:
        print(f"[WARNING] Could not load config: {e}")
        print("[INFO] Using optimized defaults...\n")
        
        cfg = FiltersConfig(
            min_liquidity_usd=3000,
            max_liquidity_usd=750000,
            min_price_usd=0.0000001,
            max_price_usd=0.10,
            min_holders=50,
            max_age_minutes=720,
            min_dex_trades_5m=5,
            min_volume_usd_1h=500,
            require_contract_verified=False,
            require_owner_renounced_or_timelock=False,
            require_mint_authority_revoked=True,
        )


    asyncio.run(main(cfg))
