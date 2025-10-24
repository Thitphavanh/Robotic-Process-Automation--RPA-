"""
AI Agent Service for Dynamic Market Discovery
Uses Claude AI (Anthropic) to intelligently discover and analyze market data
"""

import os
import json
import anthropic
from datetime import datetime
from typing import List, Dict, Tuple


class ClaudeAIAgent:
    """
    AI Agent ที่ใช้ Claude AI ในการค้นหาและวิเคราะห์ข้อมูลตลาดแบบ Dynamic Real-time
    """

    def __init__(self):
        self.api_key = os.environ.get('ANTHROPIC_API_KEY', '')
        self.use_claude = bool(self.api_key)

        if self.use_claude:
            self.client = anthropic.Anthropic(api_key=self.api_key)
            self.model = "claude-3-5-sonnet-20241022"  # Latest Claude model
            print("✓ Claude AI Agent initialized successfully")
        else:
            self.client = None
            print("⚠ Warning: ANTHROPIC_API_KEY not found. AI Agent features disabled.")

    def discover_top_stocks(self, market: str, limit: int = 10) -> List[Tuple[str, str]]:
        """
        ค้นหาหุ้น Top ของตลาดแบบ Dynamic ด้วย Claude AI

        Args:
            market: 'thai', 'us', 'europe', 'china'
            limit: จำนวนหุ้นที่ต้องการ (default 10)

        Returns:
            List of tuples: [(symbol, company_name), ...]
        """
        if not self.use_claude:
            return self._get_fallback_stocks(market, limit)

        try:
            prompt = self._create_stock_discovery_prompt(market, limit)

            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.1,  # Low temperature for consistent results
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            response_text = message.content[0].text
            stocks = self._parse_stock_response(response_text, market)

            print(f"✓ Claude AI discovered {len(stocks)} {market} stocks")
            return stocks[:limit]

        except Exception as e:
            print(f"✗ Error in Claude AI stock discovery: {e}")
            return self._get_fallback_stocks(market, limit)

    def discover_top_crypto(self, limit: int = 10) -> List[Dict[str, str]]:
        """
        ค้นหา Crypto Top แบบ Dynamic ด้วย Claude AI

        Args:
            limit: จำนวน crypto ที่ต้องการ (default 10)

        Returns:
            List of dicts: [{'id': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'BTC'}, ...]
        """
        if not self.use_claude:
            return self._get_fallback_crypto(limit)

        try:
            prompt = self._create_crypto_discovery_prompt(limit)

            message = self.client.messages.create(
                model=self.model,
                max_tokens=2000,
                temperature=0.1,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ]
            )

            response_text = message.content[0].text
            cryptos = self._parse_crypto_response(response_text)

            print(f"✓ Claude AI discovered {len(cryptos)} cryptocurrencies")
            return cryptos[:limit]

        except Exception as e:
            print(f"✗ Error in Claude AI crypto discovery: {e}")
            return self._get_fallback_crypto(limit)

    def analyze_market_sentiment(self, market: str) -> Dict[str, any]:
        """
        วิเคราะห์ Market Sentiment ด้วย Claude AI

        Args:
            market: 'thai', 'us', 'europe', 'china', 'crypto'

        Returns:
            Dict with sentiment analysis
        """
        if not self.use_claude:
            return {"sentiment": "neutral", "confidence": 0.5, "summary": "AI Agent not available"}

        try:
            prompt = f"""Analyze the current market sentiment for {market} market as of {datetime.now().strftime('%Y-%m-%d')}.

Provide:
1. Overall sentiment (bullish/bearish/neutral)
2. Confidence level (0-1)
3. Key factors affecting the market
4. Brief summary (2-3 sentences in Thai)

Return as JSON format:
{{
    "sentiment": "bullish/bearish/neutral",
    "confidence": 0.0-1.0,
    "key_factors": ["factor1", "factor2", "factor3"],
    "summary": "สรุปภาษาไทย..."
}}"""

            message = self.client.messages.create(
                model=self.model,
                max_tokens=1500,
                temperature=0.3,
                messages=[{"role": "user", "content": prompt}]
            )

            response_text = message.content[0].text

            # Extract JSON from response
            json_start = response_text.find('{')
            json_end = response_text.rfind('}') + 1
            if json_start != -1 and json_end > json_start:
                sentiment_data = json.loads(response_text[json_start:json_end])
                return sentiment_data
            else:
                return {"sentiment": "neutral", "confidence": 0.5, "summary": "Unable to parse response"}

        except Exception as e:
            print(f"✗ Error in sentiment analysis: {e}")
            return {"sentiment": "neutral", "confidence": 0.5, "summary": f"Error: {str(e)}"}

    def _create_stock_discovery_prompt(self, market: str, limit: int) -> str:
        """สร้าง prompt สำหรับค้นหาหุ้น"""

        market_info = {
            'thai': {
                'name': 'Thai Stock Exchange (SET)',
                'suffix': '.BK',
                'examples': 'PTT.BK, CPALL.BK, AOT.BK'
            },
            'us': {
                'name': 'US Stock Market (NYSE/NASDAQ)',
                'suffix': '',
                'examples': 'AAPL, MSFT, GOOGL'
            },
            'europe': {
                'name': 'European Stock Markets',
                'suffix': '',
                'examples': 'MC.PA (France), ASML.AS (Netherlands), SAP (Germany)'
            },
            'china': {
                'name': 'Chinese Stock Markets (SSE/SZSE)',
                'suffix': '.SS or .SZ',
                'examples': '600519.SS, 000858.SZ, 000333.SZ'
            }
        }

        info = market_info.get(market, market_info['us'])

        return f"""You are a financial market expert. Provide the TOP {limit} most valuable and actively traded stocks in the {info['name']} based on current market capitalization and trading volume.

Requirements:
1. Return ONLY the top {limit} stocks
2. Use correct ticker symbols with appropriate suffixes (e.g., {info['suffix']})
3. Include company names in their local language where appropriate
4. Format: symbol|company_name (one per line)
5. Order by market capitalization (largest first)

Example format:
{info['examples']}

Current date: {datetime.now().strftime('%Y-%m-%d')}

Please provide the list now:"""

    def _create_crypto_discovery_prompt(self, limit: int) -> str:
        """สร้าง prompt สำหรับค้นหา Crypto"""

        return f"""You are a cryptocurrency market expert. Provide the TOP {limit} cryptocurrencies by market capitalization as of {datetime.now().strftime('%Y-%m-%d')}.

Requirements:
1. Return ONLY the top {limit} cryptocurrencies
2. Use CoinGecko API IDs (lowercase, hyphenated)
3. Include full name and symbol
4. Format: id|name|symbol (one per line)
5. Order by market capitalization (largest first)

Example format:
bitcoin|Bitcoin|BTC
ethereum|Ethereum|ETH
tether|Tether|USDT

Please provide the list now:"""

    def _parse_stock_response(self, response: str, market: str) -> List[Tuple[str, str]]:
        """แปลง response จาก Claude เป็นรายการหุ้น"""
        stocks = []
        lines = response.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('**'):
                continue

            # Remove numbering (1., 2., etc.)
            line = line.lstrip('0123456789.)')
            line = line.strip()

            # Parse different formats
            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 2:
                    symbol = parts[0].strip()
                    name = parts[1].strip()
                    stocks.append((symbol, name))
            elif ' - ' in line:
                parts = line.split(' - ')
                if len(parts) >= 2:
                    symbol = parts[0].strip()
                    name = parts[1].strip()
                    stocks.append((symbol, name))
            elif '\t' in line:
                parts = line.split('\t')
                if len(parts) >= 2:
                    symbol = parts[0].strip()
                    name = parts[1].strip()
                    stocks.append((symbol, name))

        return stocks

    def _parse_crypto_response(self, response: str) -> List[Dict[str, str]]:
        """แปลง response จาก Claude เป็นรายการ Crypto"""
        cryptos = []
        lines = response.strip().split('\n')

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#') or line.startswith('**'):
                continue

            # Remove numbering
            line = line.lstrip('0123456789.)')
            line = line.strip()

            if '|' in line:
                parts = line.split('|')
                if len(parts) >= 3:
                    crypto_id = parts[0].strip().lower()
                    name = parts[1].strip()
                    symbol = parts[2].strip().upper()
                    cryptos.append({
                        'id': crypto_id,
                        'name': name,
                        'symbol': symbol
                    })

        return cryptos

    def _get_fallback_stocks(self, market: str, limit: int) -> List[Tuple[str, str]]:
        """Fallback stocks when AI is not available"""
        fallback_data = {
            'thai': [
                ('PTT.BK', 'ปตท.'),
                ('CPALL.BK', 'ซีพีออลล์'),
                ('AOT.BK', 'ท่าอากาศยาน'),
                ('KBANK.BK', 'ธนาคารกสิกรไทย'),
                ('SCB.BK', 'ธนาคารไทยพาณิชย์'),
                ('BBL.BK', 'ธนาคารกรุงเทพ'),
                ('ADVANC.BK', 'แอดวานซ์ อินโฟร์ เซอร์วิส'),
                ('TRUE.BK', 'ทรู คอร์ปอเรชั่น'),
                ('GULF.BK', 'กัลฟ์ เอ็นเนอร์จี'),
                ('PTTEP.BK', 'ปตท.สผ.')
            ],
            'us': [
                ('AAPL', 'Apple'),
                ('MSFT', 'Microsoft'),
                ('GOOGL', 'Alphabet'),
                ('AMZN', 'Amazon'),
                ('NVDA', 'NVIDIA'),
                ('TSLA', 'Tesla'),
                ('META', 'Meta'),
                ('BRK-B', 'Berkshire Hathaway'),
                ('JPM', 'JPMorgan Chase'),
                ('V', 'Visa')
            ],
            'europe': [
                ('MC.PA', 'LVMH'),
                ('ASML.AS', 'ASML'),
                ('NVO', 'Novo Nordisk'),
                ('SAP', 'SAP'),
                ('OR.PA', "L'Oréal"),
                ('SAN.PA', 'Sanofi'),
                ('SIE.DE', 'Siemens'),
                ('NESN.SW', 'Nestlé'),
                ('NOVN.SW', 'Novartis'),
                ('SHEL.L', 'Shell')
            ],
            'china': [
                ('600519.SS', 'Kweichow Moutai'),
                ('000858.SZ', 'Wuliangye Yibin'),
                ('000333.SZ', 'Midea Group'),
                ('601318.SS', 'Ping An Insurance'),
                ('600036.SS', 'China Merchants Bank'),
                ('000001.SZ', 'Ping An Bank'),
                ('601888.SS', 'China Tourism Group'),
                ('600887.SS', 'Inner Mongolia Yili'),
                ('000568.SZ', 'Luzhou Laojiao'),
                ('601012.SS', 'Longfor Group')
            ]
        }

        return fallback_data.get(market, fallback_data['us'])[:limit]

    def _get_fallback_crypto(self, limit: int) -> List[Dict[str, str]]:
        """Fallback crypto when AI is not available"""
        fallback = [
            {'id': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'BTC'},
            {'id': 'ethereum', 'name': 'Ethereum', 'symbol': 'ETH'},
            {'id': 'tether', 'name': 'Tether', 'symbol': 'USDT'},
            {'id': 'binancecoin', 'name': 'BNB', 'symbol': 'BNB'},
            {'id': 'solana', 'name': 'Solana', 'symbol': 'SOL'},
            {'id': 'ripple', 'name': 'XRP', 'symbol': 'XRP'},
            {'id': 'usd-coin', 'name': 'USDC', 'symbol': 'USDC'},
            {'id': 'cardano', 'name': 'Cardano', 'symbol': 'ADA'},
            {'id': 'dogecoin', 'name': 'Dogecoin', 'symbol': 'DOGE'},
            {'id': 'tron', 'name': 'TRON', 'symbol': 'TRX'}
        ]
        return fallback[:limit]


# Singleton instance
_agent_instance = None

def get_ai_agent() -> ClaudeAIAgent:
    """Get singleton instance of AI Agent"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = ClaudeAIAgent()
    return _agent_instance
