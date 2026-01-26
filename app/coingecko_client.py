import asyncio
from typing import Dict, Optional, List
from pycoingecko import CoinGeckoAPI
import logging

logger = logging.getLogger(__name__)


class CoinGeckoClient:
    """Client for fetching additional token data from CoinGecko API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize CoinGecko client
        
        Args:
            api_key: Optional API key for higher rate limits (None works for free)
        """
        if api_key:
            self.cg = CoinGeckoAPI(api_key=api_key)
        else:
            # Works without API key - lower rate limits but FREE
            self.cg = CoinGeckoAPI()
        
        self.rate_limit_delay = 2.0  # Free tier: ~30 calls/min = 2 sec delay
        logger.info("CoinGecko client initialized")
    
    async def get_token_data(self, solana_address: str) -> Optional[Dict]:
        """
        Fetch detailed token data from CoinGecko by Solana contract address
        
        Args:
            solana_address: Solana token contract address
            
        Returns:
            Dictionary with token data or None if not found
        """
        try:
            # Rate limit handling
            await asyncio.sleep(self.rate_limit_delay)
            
            # Fetch token by contract address on Solana network
            data = self.cg.get_coin_info_from_contract_address_by_id(
                id='solana',
                contract_address=solana_address
            )
            
            if not data:
                logger.debug(f"No CoinGecko data found for {solana_address}")
                return None
            
            # Extract market data
            market_data = data.get('market_data', {})
            links = data.get('links', {})
            community_data = data.get('community_data', {})
            
            result = {
                'name': data.get('name'),
                'symbol': data.get('symbol', '').upper(),
                'coingecko_id': data.get('id'),
                
                # Price data
                'price_usd': market_data.get('current_price', {}).get('usd'),
                'market_cap': market_data.get('market_cap', {}).get('usd'),
                'fully_diluted_valuation': market_data.get('fully_diluted_valuation', {}).get('usd'),
                'volume_24h': market_data.get('total_volume', {}).get('usd'),
                
                # Price changes
                'price_change_24h': market_data.get('price_change_percentage_24h'),
                'price_change_7d': market_data.get('price_change_percentage_7d'),
                'price_change_30d': market_data.get('price_change_percentage_30d'),
                
                # All-time high
                'ath': market_data.get('ath', {}).get('usd'),
                'ath_change_percentage': market_data.get('ath_change_percentage', {}).get('usd'),
                'ath_date': market_data.get('ath_date', {}).get('usd'),
                
                # All-time low
                'atl': market_data.get('atl', {}).get('usd'),
                'atl_change_percentage': market_data.get('atl_change_percentage', {}).get('usd'),
                
                # Supply data
                'circulating_supply': market_data.get('circulating_supply'),
                'total_supply': market_data.get('total_supply'),
                'max_supply': market_data.get('max_supply'),
                
                # Rankings and scores
                'coingecko_rank': data.get('market_cap_rank'),
                'coingecko_score': data.get('coingecko_score'),
                'developer_score': data.get('developer_score'),
                'community_score': data.get('community_score'),
                'liquidity_score': data.get('liquidity_score'),
                'public_interest_score': data.get('public_interest_score'),
                
                # Social and links
                'links': {
                    'homepage': links.get('homepage', [])[0] if links.get('homepage') else None,
                    'twitter': links.get('twitter_screen_name'),
                    'telegram': links.get('telegram_channel_identifier'),
                    'discord': links.get('chat_url', [])[0] if links.get('chat_url') else None,
                    'github': links.get('repos_url', {}).get('github', [])[0] if links.get('repos_url', {}).get('github') else None,
                },
                
                # Community data
                'twitter_followers': community_data.get('twitter_followers'),
                'telegram_users': community_data.get('telegram_channel_user_count'),
                
                # Description
                'description': data.get('description', {}).get('en', '')[:500] if data.get('description') else None,
            }
            
            logger.info(f"Fetched CoinGecko data for {result['symbol']} ({solana_address})")
            return result
            
        except Exception as e:
            logger.error(f"Error fetching CoinGecko data for {solana_address}: {e}")
            return None
    
    async def get_trending_tokens(self) -> Optional[List[Dict]]:
        """
        Fetch currently trending tokens from CoinGecko
        
        Returns:
            List of trending token data or None if error
        """
        try:
            await asyncio.sleep(self.rate_limit_delay)
            
            trending = self.cg.get_search_trending()
            coins = trending.get('coins', [])
            
            logger.info(f"Fetched {len(coins)} trending tokens from CoinGecko")
            return coins
            
        except Exception as e:
            logger.error(f"Error fetching trending tokens: {e}")
            return None
    
    async def ping(self) -> bool:
        """
        Check if CoinGecko API is responsive
        
        Returns:
            True if API is working, False otherwise
        """
        try:
            response = self.cg.ping()
            return response.get('gecko_says') == '(V3) To the Moon!'
        except Exception as e:
            logger.error(f"CoinGecko ping failed: {e}")
            return False


# Example usage and testing
if __name__ == "__main__":
    async def test():
        print("Testing CoinGecko client...")
        
        # PLUG AND PLAY - No API key needed!
        client = CoinGeckoClient()
        
        # Test 1: Ping
        print("\n1. Testing API connection...")
        is_alive = await client.ping()
        print(f"   CoinGecko API alive: {is_alive}")
        
        # Test 2: Get token data (Raydium - known Solana token)
        print("\n2. Testing token data fetch...")
        raydium_address = "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R"
        data = await client.get_token_data(raydium_address)
        
        if data:
            print(f"   ✅ Token: {data['name']} ({data['symbol']})")
            print(f"   Price: ${data['price_usd']}")
            if data['market_cap']:
                print(f"   Market Cap: ${data['market_cap']:,.0f}")
            if data['price_change_24h']:
                print(f"   24h Change: {data['price_change_24h']:.2f}%")
            print(f"   CoinGecko Score: {data['coingecko_score']}")
            print(f"   Community Score: {data['community_score']}")
        else:
            print("   ❌ No data returned")
        
        # Test 3: Trending tokens
        print("\n3. Testing trending tokens...")
        trending = await client.get_trending_tokens()
        if trending:
            print(f"   Top 3 trending:")
            for i, coin in enumerate(trending[:3], 1):
                item = coin.get('item', {})
                print(f"   {i}. {item.get('name')} ({item.get('symbol')})")
        
        print("\n✅ All tests complete!")
    
    asyncio.run(test())
