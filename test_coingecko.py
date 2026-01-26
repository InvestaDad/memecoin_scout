import asyncio
import sys
from app.coingecko_client import CoinGeckoClient

async def test_coingecko():
    """Test CoinGecko integration with real Solana tokens"""
    
    print("\n" + "="*70)
    print("🔍 TESTING COINGECKO INTEGRATION")
    print("="*70)
    
    client = CoinGeckoClient()  # No API key needed
    
    # TEST 1: API Connection
    print("\n[TEST 1] Checking CoinGecko API Connection...")
    is_alive = await client.ping()
    if is_alive:
        print("✅ CoinGecko API is LIVE and responding!")
    else:
        print("❌ CoinGecko API connection FAILED")
        return
    
    # TEST 2: Popular Solana Tokens (Should have CoinGecko data)
    print("\n[TEST 2] Testing Known Solana Tokens...")
    
    known_tokens = [
        ("4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R", "Raydium (RAY)"),
        ("JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN", "Jupiter (JUP)"),
        ("Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB", "USDT"),
    ]
    
    success_count = 0
    
    for address, name in known_tokens:
        print(f"\n  Testing: {name}")
        print(f"  Address: {address}")
        
        data = await client.get_token_data(address)
        
        if data:
            success_count += 1
            print(f"  ✅ DATA FOUND!")
            print(f"     Name: {data['name']}")
            print(f"     Symbol: {data['symbol']}")
            print(f"     Price: ${data['price_usd']}")
            
            if data['market_cap']:
                print(f"     Market Cap: ${data['market_cap']:,.0f}")
            
            if data['coingecko_score']:
                print(f"     ⭐ CoinGecko Score: {data['coingecko_score']:.2f}/100")
            
            if data['community_score']:
                print(f"     👥 Community Score: {data['community_score']:.2f}/100")
            
            if data['liquidity_score']:
                print(f"     💧 Liquidity Score: {data['liquidity_score']:.2f}/100")
            
            if data['twitter_followers']:
                print(f"     🐦 Twitter Followers: {data['twitter_followers']:,}")
            
            if data['links']['twitter']:
                print(f"     Twitter: @{data['links']['twitter']}")
        else:
            print(f"  ❌ NO DATA - Token not found on CoinGecko")
    
    # TEST 3: Trending Tokens
    print("\n[TEST 3] Fetching Trending Tokens...")
    trending = await client.get_trending_tokens()
    
    if trending and len(trending) > 0:
        print(f"✅ Found {len(trending)} trending tokens!")
        print("\n  Top 5 Trending:")
        for i, coin in enumerate(trending[:5], 1):
            item = coin.get('item', {})
            print(f"  {i}. {item.get('name')} ({item.get('symbol')}) - MC Rank: {item.get('market_cap_rank', 'N/A')}")
    else:
        print("❌ Could not fetch trending tokens")
    
    # Summary
    print("\n" + "="*70)
    print("📊 TEST SUMMARY")
    print("="*70)
    print(f"✅ Tokens Successfully Fetched: {success_count}/{len(known_tokens)}")
    print(f"✅ API Status: {'Working' if is_alive else 'Failed'}")
    print(f"✅ Trending Data: {'Available' if trending else 'Unavailable'}")
    print("="*70)
    
    if success_count == len(known_tokens):
        print("\n🎉 ALL TESTS PASSED! CoinGecko integration is WORKING!")
    else:
        print(f"\n⚠️ Only {success_count}/{len(known_tokens)} tokens found. Some may not be on CoinGecko.")
    
    print("\n")

if __name__ == "__main__":
    asyncio.run(test_coingecko())
