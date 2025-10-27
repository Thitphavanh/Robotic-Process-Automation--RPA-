"""
AI Agent Service for Dynamic Market Discovery
Uses Google Gemini AI to intelligently discover and analyze market data
"""

import os
import json
import google.generativeai as genai
from datetime import datetime
from typing import List, Dict, Tuple


class GeminiAIAgent:
    """
    AI Agent ที่ใช้ Google Gemini AI ในการค้นหาและวิเคราะห์ข้อมูลตลาดแบบ Dynamic Real-time
    """

    def __init__(self):
        self.api_key = os.environ.get('GEMINI_API_KEY', '')
        self.use_gemini = bool(self.api_key)

        if self.use_gemini:
            genai.configure(api_key=self.api_key)
            # Use gemini-pro as the stable model
            # Note: Model availability may vary by API key and region
            self.model = genai.GenerativeModel('gemini-pro')
            print("✓ Gemini AI Agent initialized (using fallback for stock discovery due to API limitations)")
        else:
            self.model = None
            print("⚠ Warning: GEMINI_API_KEY not found. AI Agent features disabled.")

    def discover_top_stocks(self, market: str, limit: int = 20) -> List[Tuple[str, str]]:
        """
        ค้นหาหุ้น Top ของตลาดแบบ Dynamic ด้วย Gemini AI

        Note: Due to API limitations, currently using curated fallback data

        Args:
            market: 'thai', 'us', 'europe', 'china'
            limit: จำนวนหุ้นที่ต้องการ (default 10)

        Returns:
            List of tuples: [(symbol, company_name), ...]
        """
        # Use fallback data directly for now due to Gemini API model availability issues
        # The fallback data is curated and updated regularly
        return self._get_fallback_stocks(market, limit)

    def discover_top_crypto(self, limit: int = 10) -> List[Dict[str, str]]:
        """
        ค้นหา Crypto Top แบบ Dynamic ด้วย Gemini AI

        Args:
            limit: จำนวน crypto ที่ต้องการ (default 10)

        Returns:
            List of dicts: [{'id': 'bitcoin', 'name': 'Bitcoin', 'symbol': 'BTC'}, ...]
        """
        if not self.use_gemini:
            return self._get_fallback_crypto(limit)

        try:
            prompt = self._create_crypto_discovery_prompt(limit)

            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.1,
                    'max_output_tokens': 2000,
                }
            )

            response_text = response.text
            cryptos = self._parse_crypto_response(response_text)

            print(f"✓ Gemini AI discovered {len(cryptos)} cryptocurrencies")
            return cryptos[:limit]

        except Exception as e:
            print(f"✗ Error in Gemini AI crypto discovery: {e}")
            return self._get_fallback_crypto(limit)

    def analyze_market_sentiment(self, market: str) -> Dict[str, any]:
        """
        วิเคราะห์ Market Sentiment ด้วย Gemini AI

        Args:
            market: 'thai', 'us', 'europe', 'china', 'crypto'

        Returns:
            Dict with sentiment analysis
        """
        if not self.use_gemini:
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

            response = self.model.generate_content(
                prompt,
                generation_config={
                    'temperature': 0.3,
                    'max_output_tokens': 1500,
                }
            )

            response_text = response.text

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
                ('PTTEP.BK', 'ปตท.สผ.'),
                ('BGRIM.BK', 'บี.กริม เพาเวอร์'),
                ('GPSC.BK', 'โกลบอล เพาเวอร์ ซินเนอร์ยี่'),
                ('TOP.BK', 'ไทยออยล์'),
                ('CPN.BK', 'เซ็นทรัลพัฒนา'),
                ('AWC.BK', 'แอสเสท เวิรด์'),
                ('WHA.BK', 'ดับบลิวเอชเอ คอร์ปอเรชั่น'),
                ('INTUCH.BK', 'อินทัช โฮลดิ้งส์'),
                ('DTAC.BK', 'ดีแทค'),
                ('COM7.BK', 'คอมเซเว่น'),
                ('HMPRO.BK', 'โฮม โปรดักส์ เซ็นเตอร์')
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
                ('V', 'Visa'),
                ('UNH', 'UnitedHealth'),
                ('MA', 'Mastercard'),
                ('PG', 'Procter & Gamble'),
                ('JNJ', 'Johnson & Johnson'),
                ('HD', 'Home Depot'),
                ('XOM', 'Exxon Mobil'),
                ('CVX', 'Chevron'),
                ('LLY', 'Eli Lilly'),
                ('ABBV', 'AbbVie'),
                ('PFE', 'Pfizer')
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
                ('SHEL.L', 'Shell'),
                ('TTE.PA', 'TotalEnergies'),
                ('AZN', 'AstraZeneca'),
                ('ROG.SW', 'Roche'),
                ('INGA.AS', 'ING Group'),
                ('SU.PA', 'Schneider Electric'),
                ('AIR.PA', 'Airbus'),
                ('EQNR.OL', 'Equinor'),
                ('VNA.DE', 'Vonovia'),
                ('BAS.DE', 'BASF'),
                ('DTE.DE', 'Deutsche Telekom')
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
                ('601012.SS', 'Longfor Group'),
                ('600276.SS', 'Jiangsu Hengrui Medicine'),
                ('000725.SZ', 'BOE Technology'),
                ('002594.SZ', 'BYD Company'),
                ('000002.SZ', 'China Vanke'),
                ('600900.SS', 'China Yangtze Power'),
                ('601166.SS', 'Industrial Bank'),
                ('600030.SS', 'CITIC Securities'),
                ('600104.SS', 'SAIC Motor'),
                ('601988.SS', 'Bank of China'),
                ('601398.SS', 'ICBC')
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

def get_ai_agent() -> GeminiAIAgent:
    """Get singleton instance of AI Agent"""
    global _agent_instance
    if _agent_instance is None:
        _agent_instance = GeminiAIAgent()
    return _agent_instance
