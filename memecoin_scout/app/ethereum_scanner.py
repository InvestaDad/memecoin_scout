"""
Ethereum Smart Contract Security Scanner
Multi-layer detection: Web3.py + GoPlus API + Etherscan
"""
from web3 import Web3
import os
import requests
from typing import Dict, List
import yaml
from dotenv import load_dotenv

load_dotenv()

# Load config from parent directory
config_path = os.path.join(os.path.dirname(__file__), '..', 'config.yaml')
with open(config_path, 'r') as f:
    config = yaml.safe_load(f)

ALCHEMY_URL = os.getenv('ALCHEMY_API_KEY')
ETHERSCAN_API = os.getenv('ETHERSCAN_API_KEY', '')

# Initialize Web3
w3 = Web3(Web3.HTTPProvider(ALCHEMY_URL))


class EthereumScanner:
    """Ethereum contract scanner - mirrors your Solana scanner architecture"""
    
    def __init__(self):
        self.w3 = w3
        self.goplus_enabled = config.get('goplus', {}).get('enabled', True)
    
    def scan_contract(self, address: str) -> Dict:
        """Main scanning function - returns unified risk assessment"""
        try:
            checksum_address = self.w3.to_checksum_address(address)
            
            # Basic contract check
            code = self.w3.eth.get_code(checksum_address)
            is_contract = len(code) > 0
            
            if not is_contract:
                return self._wallet_response(checksum_address)
            
            # Multi-layer security analysis
            goplus_data = self._scan_with_goplus(checksum_address)
            is_verified = self._check_verification(checksum_address)
            
            # Calculate risk score (0-100)
            risk_score = self._calculate_risk_score(goplus_data, is_verified, len(code.hex()))
            flags = self._build_flags(goplus_data, is_verified)
            verdict = self._get_verdict(risk_score)
            
            return {
                'chain': 'ethereum',
                'address': checksum_address,
                'is_contract': True,
                'risk_score': risk_score,
                'verdict': verdict,
                'checks': {
                    'bytecode_length': len(code.hex()),
                    'verified': is_verified,
                    'goplus_data': goplus_data
                },
                'flags': flags,
                'recommendations': self._get_recommendations(risk_score)
            }
            
        except Exception as e:
            return {
                'error': str(e),
                'chain': 'ethereum',
                'address': address
            }
    
    def _wallet_response(self, address: str) -> Dict:
        """Return safe response for wallet addresses"""
        return {
            'chain': 'ethereum',
            'address': address,
            'is_contract': False,
            'risk_score': 0,
            'verdict': 'SAFE - Wallet Address',
            'checks': {'type': 'wallet'},
            'flags': []
        }
    
    def _scan_with_goplus(self, address: str) -> Dict:
        """GoPlus Security API integration"""
        if not self.goplus_enabled:
            return {}
        
        url = f"https://api.gopluslabs.io/api/v1/token_security/1?contract_addresses={address}"
        
        try:
            response = requests.get(url, timeout=10)
            data = response.json()
            
            if 'result' in data and address.lower() in data['result']:
                token = data['result'][address.lower()]
                return {
                    'is_honeypot': token.get('is_honeypot', '0') == '1',
                    'buy_tax': float(token.get('buy_tax', '0')),
                    'sell_tax': float(token.get('sell_tax', '0')),
                    'is_open_source': token.get('is_open_source', '0') == '1',
                    'is_proxy': token.get('is_proxy', '0') == '1',
                    'is_mintable': token.get('is_mintable', '0') == '1',
                    'can_take_back_ownership': token.get('can_take_back_ownership', '0') == '1',
                    'owner_change_balance': token.get('owner_change_balance', '0') == '1',
                    'hidden_owner': token.get('hidden_owner', '0') == '1',
                    'selfdestruct': token.get('selfdestruct', '0') == '1',
                    'holder_count': int(token.get('holder_count', '0')),
                    'lp_holder_count': int(token.get('lp_holder_count', '0'))
                }
        except Exception as e:
            print(f"GoPlus API error: {e}")
        
        return {}
    
    def _check_verification(self, address: str) -> bool:
        """Check Etherscan verification status"""
        if not ETHERSCAN_API:
            return None
        
        url = f"https://api.etherscan.io/api?module=contract&action=getsourcecode&address={address}&apikey={ETHERSCAN_API}"
        
        try:
            response = requests.get(url, timeout=5)
            data = response.json()
            return data['result'][0]['SourceCode'] != ''
        except:
            return None
    
    def _calculate_risk_score(self, goplus_data: Dict, is_verified: bool, bytecode_length: int) -> int:
        """Calculate 0-100 risk score"""
        risk = 0
        
        if not goplus_data:
            if not is_verified:
                risk += 40
            if bytecode_length < 1000:
                risk += 30
            return min(risk, 100)
        
        # Critical flags
        if goplus_data.get('is_honeypot'):
            return 100
        if goplus_data.get('selfdestruct'):
            risk += 80
        if goplus_data.get('hidden_owner'):
            risk += 60
        if goplus_data.get('owner_change_balance'):
            risk += 70
        
        # High-risk flags
        if goplus_data.get('can_take_back_ownership'):
            risk += 40
        if goplus_data.get('is_mintable'):
            risk += 30
        
        # Tax analysis
        sell_tax = goplus_data.get('sell_tax', 0)
        buy_tax = goplus_data.get('buy_tax', 0)
        
        if sell_tax > 0.5:
            risk += 50
        elif sell_tax > 0.2:
            risk += 30
        elif sell_tax > 0.1:
            risk += 15
        
        if buy_tax > 0.1:
            risk += 20
        
        # Verification
        if not is_verified and not goplus_data.get('is_open_source'):
            risk += 35
        
        # Holder count
        holder_count = goplus_data.get('holder_count', 0)
        if holder_count < 10:
            risk += 25
        elif holder_count < 50:
            risk += 15
        
        return min(risk, 100)
    
    def _build_flags(self, goplus_data: Dict, is_verified: bool) -> List[str]:
        """Generate security warning flags"""
        flags = []
        
        if not goplus_data:
            if not is_verified:
                flags.append('[CRITICAL] Unverified source code')
            return flags
        
        # Critical warnings
        if goplus_data.get('is_honeypot'):
            flags.append('[CRITICAL] HONEYPOT DETECTED - Cannot sell')
        if goplus_data.get('selfdestruct'):
            flags.append('[CRITICAL] Can self-destruct contract')
        if goplus_data.get('hidden_owner'):
            flags.append('[CRITICAL] Hidden owner detected')
        if goplus_data.get('owner_change_balance'):
            flags.append('[CRITICAL] Owner can modify balances')
        
        # High-risk flags
        if goplus_data.get('can_take_back_ownership'):
            flags.append('[HIGH] Can reclaim ownership')
        if goplus_data.get('is_mintable'):
            flags.append('[HIGH] Unlimited minting possible')
        if goplus_data.get('is_proxy'):
            flags.append('[MEDIUM] Proxy contract - logic can change')
        
        # Tax warnings
        sell_tax = goplus_data.get('sell_tax', 0)
        buy_tax = goplus_data.get('buy_tax', 0)
        
        if sell_tax > 0.5:
            flags.append(f'[CRITICAL] EXTREME sell tax: {sell_tax*100:.1f}%')
        elif sell_tax > 0.2:
            flags.append(f'[HIGH] High sell tax: {sell_tax*100:.1f}%')
        elif sell_tax > 0.05:
            flags.append(f'[MEDIUM] Moderate sell tax: {sell_tax*100:.1f}%')
        
        if buy_tax > 0.1:
            flags.append(f'[HIGH] High buy tax: {buy_tax*100:.1f}%')
        
        # Verification
        if not is_verified and not goplus_data.get('is_open_source'):
            flags.append('[MEDIUM] Source code not verified')
        
        # Holder count
        holder_count = goplus_data.get('holder_count', 0)
        if holder_count < 10:
            flags.append(f'[HIGH] Very few holders: {holder_count}')
        elif holder_count < 50:
            flags.append(f'[MEDIUM] Low holder count: {holder_count}')
        
        return flags
    
    def _get_verdict(self, risk_score: int) -> str:
        """Generate verdict based on risk score"""
        if risk_score >= 80:
            return 'EXTREME DANGER - DO NOT BUY'
        elif risk_score >= 60:
            return 'HIGH RISK - Likely Scam'
        elif risk_score >= 30:
            return 'CAUTION - Verify Manually'
        else:
            return 'APPEARS SAFE'
    
    def _get_recommendations(self, risk_score: int) -> List[str]:
        """Generate actionable recommendations"""
        if risk_score >= 80:
            return [
                "DO NOT INVEST - High probability of scam",
                "Report this token to the community"
            ]
        elif risk_score >= 60:
            return ["AVOID - Multiple red flags detected"]
        elif risk_score >= 30:
            return [
                "Proceed with extreme caution",
                "Verify on multiple scanners before investing"
            ]
        else:
            return [
                "Token appears legitimate",
                "Always DYOR - check liquidity and holder distribution"
            ]


# Singleton instance
ethereum_scanner = EthereumScanner()


def scan_ethereum_contract(address: str) -> Dict:
    """Main entry point for Ethereum scanning"""
    return ethereum_scanner.scan_contract(address)
