"""
News Scraper Service - ดึงข้อมูลข่าวจากหลายแหล่ง (10 รายการล่าสุดต่อหมวด)
Uses AI Agent for Dynamic Market Discovery + Trusted News Sources

Stock Categories (Use Gemini AI Agent + yfinance for real-time data):
- หุ้นไทย (Thai Stocks): Data from Yahoo Finance, reference sites: www.set.or.th, www.settrade.com, www.kaohoon.com, stock.gapfocus.com, www.investing.com
- หุ้นอเมริกา (US Stocks): Data from Yahoo Finance, reference sites: www.sec.gov, www.nyse.com, www.nasdaq.com, www.bloomberg.com, www.reuters.com, www.wsj.com, finance.yahoo.com, www.google.com/finance, www.marketwatch.com
- หุ้นยุโรป (Europe Stocks): Data from Yahoo Finance, reference sites: www.euronext.com, www.londonstockexchange.com, www.deutsche-boerse.com, www.boerse-frankfurt.de, www.ft.com, www.degiro.com
- หุ้นจีน (China Stocks): Data from Yahoo Finance, reference sites: www.hkex.com.hk, www.hsi.com.hk, www.sfc.hk, english.sse.com.cn, www.szse.cn/English/, www.spglobal.com/spdji/

News Categories (Web scraping from trusted sources):
- Bitcoin/Crypto: CoinGecko API + news from coindesk.com, cointelegraph.com, coinbase.com, binance.com, etc.
- ราคาทองคำ (Gold): yfinance data + news from gold.org, bullionvault.com, kitco.com, bloomberg.com, investing.com
- Technology AI: news.mit.edu, ai.stanford.edu, openai.com, ai.google, deepmind.google, ai.meta.com, developer.nvidia.com, etc.
- Hardware: tomshardware.com, techspot.com, anandtech.com, pcmag.com, kitguru.net, wccftech.com, techpowerup.com, etc.
- Software: github.com, stackoverflow.com, dev.to, hashnode.com, g2.com, capterra.com, trustradius.com, cnet.com, etc.
- Football: livescore.com, espn.com, skysports.com, bbc.com, goal.com, premierleague.com, uefa.com, laliga.com, legaseriea.it, bundesliga.com
- EV Car: insideevs.com, thedriven.io, electrek.co, evmagazine.com, etc.
- Rocket & Space: nasa.gov, esa.int, spacex.com, spaceflightnow.com, nasaspaceflight.com, space.com, planetary.org
- E-Commerce Deals: lazada.co.th, shopee.co.th, taobao.com, tmall.com, pinduoduo.com, alibaba.com, amazon.com, tiktok.com
"""
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from django.utils import timezone
from .models import NewsSource, NewsArticle
from .ai_agent import get_ai_agent
import urllib3

# Disable SSL warnings for sites with certificate issues
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False
    print("Warning: yfinance not installed. Stock scraping will use fallback method.")


class NewsScraperService:
    """Service สำหรับดึงข้อมูลข่าว - 10 รายการล่าสุดต่อหมวด"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }
        self.ai_agent = get_ai_agent()  # Initialize AI Agent
        print("🤖 AI Agent initialized for dynamic market discovery")

    def scrape_all_categories(self):
        """ดึงข้อมูลข่าวทุกหมวดหมู่ - 10 รายการล่าสุดต่อหมวด"""
        results = {}

        # ดึงข้อมูลหุ้นไทย (10 บริษัท)
        results['stock_thai'] = self.scrape_thai_stocks()

        # ดึงข้อมูลหุ้นต่างประเทศ (อเมริกา ยุโรป จีน - 10 บริษัทต่อประเทศ)
        results['stock_us'] = self.scrape_us_stocks()
        results['stock_europe'] = self.scrape_europe_stocks()
        results['stock_china'] = self.scrape_china_stocks()

        # ดึงข้อมูล Bitcoin/Crypto (10 สกุล)
        results['crypto'] = self.scrape_crypto()

        # ดึงข้อมูลราคาทอง
        results['gold'] = self.scrape_gold()

        # ดึงข้อมูลข่าว Tech (10 ข่าวต่อหมวด)
        results['tech_ai'] = self.scrape_tech_ai()
        results['tech_hardware'] = self.scrape_tech_hardware()
        results['tech_software'] = self.scrape_tech_software()

        # ดึงข้อมูลข่าว Football (10 ข่าว)
        results['football'] = self.scrape_football_news()

        # ดึงข้อมูลข่าว EV Car (10 ข่าว)
        results['ev_car'] = self.scrape_ev_car_news()

        # ดึงข้อมูลข่าว Rocket & Space Technology (10 ข่าว)
        results['rocket_space'] = self.scrape_rocket_space_news()

        # ดึงข้อมูล E-Commerce Deals (10 ดีล)
        results['e_commerce'] = self.scrape_ecommerce_deals()

        return results

    def scrape_thai_stocks(self):
        """ดึงข้อมูลหุ้นไทย - 10 บริษัท (Dynamic Discovery with Gemini AI) + ข่าว 10 เว็บ"""
        articles = []

        # Part 1: Stock Prices from yfinance
        if YFINANCE_AVAILABLE:
            # 🤖 ใช้ Gemini AI Agent ค้นหาหุ้นไทย Top 10 แบบ Dynamic
            print("🤖 Gemini AI discovering top Thai stocks...")
            thai_stocks = self.ai_agent.discover_top_stocks(market='thai', limit=10)

            if thai_stocks:
                print(f"✓ Gemini AI discovered {len(thai_stocks)} Thai stocks")

                for symbol, name in thai_stocks:
                    try:
                        ticker = yf.Ticker(symbol)
                        history = ticker.history(period='2d')

                        if not history.empty:
                            price = history['Close'].iloc[-1]
                            prev_close = history['Close'].iloc[-2] if len(history) > 1 else price

                            change = price - prev_close
                            change_percent = (change / prev_close * 100) if prev_close > 0 else 0

                            url = f"https://finance.yahoo.com/quote/{symbol}"

                            article_data = {
                                'title': f'{name} ({symbol}) ราคา {price:.2f} บาท',
                                'content': f'หุ้น {name} ({symbol}) ราคาปัจจุบัน {price:.2f} บาท เปลี่ยนแปลง {change:+.2f} ({change_percent:+.2f}%)',
                                'url': url,
                                'price': price,
                                'change': change,
                                'change_percent': change_percent,
                                'published_at': timezone.now(),
                                'category': 'stock_thai'
                            }

                            articles.append(article_data)
                            print(f"✓ Scraped {name}: {price:.2f} บาท")

                    except Exception as e:
                        print(f"Error scraping {name}: {e}")

        # Part 2: News from 10 Thai Stock Websites
        thai_stock_sources = [
            ('https://www.set.or.th/th/market/news', 'h3 a', 'SET'),
            ('https://www.settrade.com/th/market/news', '.news-title a', 'SETTRADE'),
            ('https://th.investing.com/equities/thailand', 'a.title', 'Investing.com TH'),
            ('https://www.setsmart.com/analysis/newslist', '.headline a', 'SetSmart'),
            ('https://www.finnomena.com/stock', 'article h3 a', 'Finnomena'),
            ('https://www.intergold.co.th/news', '.news-title a', 'InterGOLD'),
            ('https://www.ylgfutures.co.th/news', 'h3 a', 'YLG'),
            ('https://www.aurora.co.th/news', '.title a', 'Aurora'),
            ('https://www.huasengheng.com/news', 'h3 a', 'Huasengheng'),
            ('https://th.tradingview.com/markets/stocks-thailand/', 'a.tv-screener__symbol', 'TradingView TH'),
        ]

        for source_url, selector, source_name in thai_stock_sources:
            try:
                response = requests.get(source_url, headers=self.headers, timeout=10, verify=False)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_links = soup.select(selector)[:1]  # 1 ข่าวต่อเว็บ

                    for link in article_links:
                        try:
                            title = link.text.strip()
                            article_url = link.get('href', '')

                            if not article_url.startswith('http'):
                                base_url = source_url.rsplit('/', 2)[0]
                                article_url = base_url + article_url

                            articles.append({
                                'title': f'[{source_name}] {title}',
                                'content': f'ข่าวหุ้นไทยจาก {source_name}: {title}',
                                'url': article_url,
                                'published_at': timezone.now(),
                                'category': 'stock_thai'
                            })
                            print(f"✓ Scraped Thai stock news from {source_name}")
                        except Exception as e:
                            print(f"Error parsing Thai stock article: {e}")
            except Exception as e:
                print(f"Error scraping Thai stock news from {source_name}: {e}")

        return articles[:20]  # Return top 20 (10 prices + 10 news)

    def scrape_us_stocks(self):
        """ดึงข้อมูลหุ้นอเมริกา - 10 บริษัท (Dynamic Discovery with Gemini AI) + ข่าว 10 เว็บ"""
        articles = []

        # Part 1: Stock Prices from yfinance
        if YFINANCE_AVAILABLE:
            # 🤖 ใช้ Gemini AI Agent ค้นหาหุ้นอเมริกา Top 10 แบบ Dynamic
            print("🤖 Gemini AI discovering top US stocks...")
            us_stocks = self.ai_agent.discover_top_stocks(market='us', limit=10)

            if us_stocks:
                print(f"✓ Gemini AI discovered {len(us_stocks)} US stocks")

                for symbol, name in us_stocks:
                    try:
                        ticker = yf.Ticker(symbol)
                        history = ticker.history(period='2d')

                        if not history.empty:
                            price = history['Close'].iloc[-1]
                            prev_close = history['Close'].iloc[-2] if len(history) > 1 else price

                            change = price - prev_close
                            change_percent = (change / prev_close * 100) if prev_close > 0 else 0

                            url = f"https://finance.yahoo.com/quote/{symbol}"

                            article_data = {
                                'title': f'{name} ({symbol}) ${price:,.2f}',
                                'content': f'หุ้น {name} ({symbol}) ราคาปัจจุบัน ${price:,.2f} เปลี่ยนแปลง {change:+.2f} ({change_percent:+.2f}%)',
                                'url': url,
                                'price': price,
                                'change': change,
                                'change_percent': change_percent,
                                'published_at': timezone.now(),
                                'category': 'stock_us'
                            }

                            articles.append(article_data)
                            print(f"✓ Scraped {name}: ${price:.2f}")

                    except Exception as e:
                        print(f"Error scraping {name}: {e}")

        # Part 2: News from 10 US Stock Websites
        us_stock_sources = [
            ('https://finance.yahoo.com/news/', 'h3 a', 'Yahoo Finance'),
            ('https://www.morningstar.com/news/market', 'article h3 a', 'Morningstar'),
            ('https://seekingalpha.com/market-news', 'article a', 'Seeking Alpha'),
            ('https://www.fool.com/investing/', '.article-title a', 'The Motley Fool'),
            ('https://www.bloomberg.com/markets', 'article h3 a', 'Bloomberg'),
            ('https://www.marketwatch.com/latest-news', 'h3.article__headline a', 'MarketWatch'),
            ('https://www.cnbc.com/stocks/', '.Card-title a', 'CNBC'),
            ('https://www.tradingview.com/markets/stocks-usa/market-movers-all-stocks/', 'a.tv-screener__symbol', 'TradingView'),
            ('https://stockanalysis.com/news/', 'h3 a', 'Stock Analysis'),
            ('https://www.benzinga.com/news', '.article-title a', 'Benzinga'),
        ]

        for source_url, selector, source_name in us_stock_sources:
            try:
                response = requests.get(source_url, headers=self.headers, timeout=10, verify=False)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_links = soup.select(selector)[:1]

                    for link in article_links:
                        try:
                            title = link.text.strip()
                            article_url = link.get('href', '')

                            if not article_url.startswith('http'):
                                base_url = source_url.rsplit('/', 2)[0]
                                article_url = base_url + article_url

                            articles.append({
                                'title': f'[{source_name}] {title}',
                                'content': f'ข่าวหุ้นอเมริกาจาก {source_name}: {title}',
                                'url': article_url,
                                'published_at': timezone.now(),
                                'category': 'stock_us'
                            })
                            print(f"✓ Scraped US stock news from {source_name}")
                        except Exception as e:
                            print(f"Error parsing US stock article: {e}")
            except Exception as e:
                print(f"Error scraping US stock news from {source_name}: {e}")

        return articles[:20]  # Return top 20 (10 prices + 10 news)

    def scrape_europe_stocks(self):
        """ดึงข้อมูลหุ้นยุโรป - 10 บริษัท (Dynamic Discovery with Gemini AI) + ข่าว 10 เว็บ"""
        articles = []

        # Part 1: Stock Prices from yfinance
        if YFINANCE_AVAILABLE:
            # 🤖 ใช้ Gemini AI Agent ค้นหาหุ้นยุโรป Top 10 แบบ Dynamic
            print("🤖 Gemini AI discovering top Europe stocks...")
            europe_stocks = self.ai_agent.discover_top_stocks(market='europe', limit=10)

            if europe_stocks:
                print(f"✓ Gemini AI discovered {len(europe_stocks)} Europe stocks")

                for symbol, name in europe_stocks:
                    try:
                        ticker = yf.Ticker(symbol)
                        history = ticker.history(period='2d')

                        if not history.empty:
                            price = history['Close'].iloc[-1]
                            prev_close = history['Close'].iloc[-2] if len(history) > 1 else price

                            change = price - prev_close
                            change_percent = (change / prev_close * 100) if prev_close > 0 else 0

                            url = f"https://finance.yahoo.com/quote/{symbol}"

                            article_data = {
                                'title': f'{name} ({symbol}) €{price:,.2f}',
                                'content': f'หุ้น {name} ({symbol}) ราคาปัจจุบัน €{price:,.2f} เปลี่ยนแปลง {change:+.2f} ({change_percent:+.2f}%)',
                                'url': url,
                                'price': price,
                                'change': change,
                                'change_percent': change_percent,
                                'published_at': timezone.now(),
                                'category': 'stock_europe'
                            }

                            articles.append(article_data)
                            print(f"✓ Scraped {name}: €{price:.2f}")

                    except Exception as e:
                        print(f"Error scraping {name}: {e}")

        # Part 2: News from 10 Europe Stock Websites
        europe_stock_sources = [
            ('https://www.euronext.com/en/news', 'h3 a', 'Euronext'),
            ('https://www.londonstockexchange.com/news', '.article-title a', 'London Stock Exchange'),
            ('https://www.boerse-frankfurt.de/nachrichten', 'h3 a', 'Deutsche Börse'),
            ('https://www.investing.com/equities/europe', 'article a.title', 'Investing.com Europe'),
            ('https://www.bloomberg.com/europe', 'article h3 a', 'Bloomberg Europe'),
            ('https://www.marketscreener.com/news/latest/', 'a.title', 'MarketScreener'),
            ('https://www.nasdaq.com/european-market-activity', 'h3 a', 'NASDAQ Nordic'),
            ('https://www.tradingview.com/markets/indices/quotes-europe/', 'a.tv-screener__symbol', 'TradingView Europe'),
            ('https://www.cnbc.com/europe-markets/', '.Card-title a', 'CNBC Europe'),
            ('https://www.ft.com/european-equities', 'a.js-teaser-heading-link', 'Financial Times'),
        ]

        for source_url, selector, source_name in europe_stock_sources:
            try:
                response = requests.get(source_url, headers=self.headers, timeout=10, verify=False)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_links = soup.select(selector)[:1]

                    for link in article_links:
                        try:
                            title = link.text.strip()
                            article_url = link.get('href', '')

                            if not article_url.startswith('http'):
                                base_url = source_url.rsplit('/', 2)[0]
                                article_url = base_url + article_url

                            articles.append({
                                'title': f'[{source_name}] {title}',
                                'content': f'ข่าวหุ้นยุโรปจาก {source_name}: {title}',
                                'url': article_url,
                                'published_at': timezone.now(),
                                'category': 'stock_europe'
                            })
                            print(f"✓ Scraped Europe stock news from {source_name}")
                        except Exception as e:
                            print(f"Error parsing Europe stock article: {e}")
            except Exception as e:
                print(f"Error scraping Europe stock news from {source_name}: {e}")

        return articles[:20]  # Return top 20 (10 prices + 10 news)

    def scrape_china_stocks(self):
        """ดึงข้อมูลหุ้นจีน - 10 บริษัท (Dynamic Discovery with Gemini AI) + ข่าว 10 เว็บ"""
        articles = []

        # Part 1: Stock Prices from yfinance
        if YFINANCE_AVAILABLE:
            # 🤖 ใช้ Gemini AI Agent ค้นหาหุ้นจีน Top 10 แบบ Dynamic
            print("🤖 Gemini AI discovering top China stocks...")
            china_stocks = self.ai_agent.discover_top_stocks(market='china', limit=10)

            if china_stocks:
                print(f"✓ Gemini AI discovered {len(china_stocks)} China stocks")

                for symbol, name in china_stocks:
                    try:
                        ticker = yf.Ticker(symbol)
                        history = ticker.history(period='2d')

                        if not history.empty:
                            price = history['Close'].iloc[-1]
                            prev_close = history['Close'].iloc[-2] if len(history) > 1 else price

                            change = price - prev_close
                            change_percent = (change / prev_close * 100) if prev_close > 0 else 0

                            url = f"https://finance.yahoo.com/quote/{symbol}"

                            article_data = {
                                'title': f'{name} ({symbol}) ${price:,.2f}',
                                'content': f'หุ้น {name} ({symbol}) ราคาปัจจุบัน ${price:,.2f} เปลี่ยนแปลง {change:+.2f} ({change_percent:+.2f}%)',
                                'url': url,
                                'price': price,
                                'change': change,
                                'change_percent': change_percent,
                                'published_at': timezone.now(),
                                'category': 'stock_china'
                            }

                            articles.append(article_data)
                            print(f"✓ Scraped {name}: ${price:.2f}")

                    except Exception as e:
                        print(f"Error scraping {name}: {e}")

        # Part 2: News from 10 China Stock Websites
        china_stock_sources = [
            ('http://english.sse.com.cn/news/', 'h3 a', 'Shanghai Stock Exchange'),
            ('http://www.szse.cn/English/', '.news-title a', 'Shenzhen Stock Exchange'),
            ('https://www.hkex.com.hk/News/Market-News', 'h3 a', 'Hong Kong Stock Exchange'),
            ('https://cn.investing.com/equities/', 'a.title', 'Investing.com China'),
            ('https://www.cnbc.com/china/', '.Card-title a', 'CNBC China'),
            ('https://www.scmp.com/business/china-business', 'h3 a', 'SCMP'),
            ('https://tradingeconomics.com/china/stock-market', '.table-hover a', 'Trading Economics'),
            ('https://www.msci.com/market-insights/china', 'article h3 a', 'MSCI China'),
            ('https://www.bloomberg.com/asia', 'article h3 a', 'Bloomberg Asia'),
            ('https://www.reuters.com/markets/asia/', 'a[data-testid="Heading"]', 'Reuters Asia'),
        ]

        for source_url, selector, source_name in china_stock_sources:
            try:
                # Use Chinese language headers for better access
                headers_cn = {**self.headers, 'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'}
                response = requests.get(source_url, headers=headers_cn, timeout=10, verify=False)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_links = soup.select(selector)[:1]

                    for link in article_links:
                        try:
                            title = link.text.strip()
                            article_url = link.get('href', '')

                            if not article_url.startswith('http'):
                                base_url = source_url.rsplit('/', 2)[0]
                                article_url = base_url + article_url

                            articles.append({
                                'title': f'[{source_name}] {title}',
                                'content': f'ข่าวหุ้นจีนจาก {source_name}: {title}',
                                'url': article_url,
                                'published_at': timezone.now(),
                                'category': 'stock_china'
                            })
                            print(f"✓ Scraped China stock news from {source_name}")
                        except Exception as e:
                            print(f"Error parsing China stock article: {e}")
            except Exception as e:
                print(f"Error scraping China stock news from {source_name}: {e}")

        return articles[:20]  # Return top 20 (10 prices + 10 news)

    def scrape_crypto(self):
        """ดึงข้อมูล Cryptocurrency - 10 เว็บ (3 ราคา + 10 ข่าว)"""
        articles = []

        # Part 1: CoinGecko API - Top 3 Cryptocurrencies
        try:
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 3,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h'
            }
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                for coin in data:
                    coin_name = coin.get('name', '')
                    symbol = coin.get('symbol', '').upper()
                    usd_price = coin.get('current_price', 0)
                    change_24h = coin.get('price_change_24h', 0)
                    change_percent = coin.get('price_change_percentage_24h', 0)
                    market_cap = coin.get('market_cap', 0)
                    image_url = coin.get('image', '')

                    articles.append({
                        'title': f'{coin_name} ({symbol}) ${usd_price:,.2f}',
                        'content': f'{coin_name} ({symbol}) ราคา ${usd_price:,.2f} | 24h: {change_percent:+.2f}% | Market Cap: ${market_cap:,.0f}',
                        'url': f'https://www.coingecko.com/en/coins/{coin.get("id", "")}',
                        'price': usd_price,
                        'change': change_24h,
                        'change_percent': change_percent,
                        'image_url': image_url,
                        'published_at': timezone.now(),
                        'category': 'crypto'
                    })
                print("✓ Scraped crypto prices from CoinGecko (3 coins)")
        except Exception as e:
            print(f"Error scraping CoinGecko: {e}")

        # Part 2: News from 10 Crypto Websites
        crypto_news_sources = [
            ('https://www.coindesk.com/', 'h3 a', 'CoinDesk'),
            ('https://www.coinbase.com/blog/', 'h3 a', 'Coinbase'),
            ('https://coinmarketcap.com/headlines/news/', '.sc-16r8icm-0 a', 'CoinMarketCap'),
            ('https://www.coingecko.com/en/news', '.news-title a', 'CoinGecko News'),
            ('https://crypto.com/news', 'article h3 a', 'Crypto.com'),
            ('https://www.binance.com/en/blog', 'article a', 'Binance'),
            ('https://www.kraken.com/learn/news', '.article-card a', 'Kraken'),
            ('https://cointelegraph.com/', 'article .title a', 'CoinTelegraph'),
            ('https://www.theblock.co/', 'article a', 'The Block'),
            ('https://decrypt.co/', 'article h3 a', 'Decrypt'),
        ]

        for source_url, selector, source_name in crypto_news_sources:
            try:
                response = requests.get(source_url, headers=self.headers, timeout=10, verify=False)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_links = soup.select(selector)[:1]

                    for link in article_links:
                        try:
                            title = link.text.strip()
                            article_url = link.get('href', '')

                            if not article_url.startswith('http'):
                                base_url = source_url.rstrip('/').split('/news')[0].split('/blog')[0].split('/headlines')[0]
                                article_url = base_url + article_url

                            articles.append({
                                'title': f'[{source_name}] {title}',
                                'content': f'ข่าว Crypto จาก {source_name}: {title}',
                                'url': article_url,
                                'published_at': timezone.now(),
                                'category': 'crypto'
                            })
                            print(f"✓ Scraped crypto news from {source_name}")

                        except Exception as e:
                            print(f"Error parsing crypto article from {source_name}: {e}")
            except Exception as e:
                print(f"Error scraping crypto news from {source_name}: {e}")

        return articles[:15]  # Top 15 (3 prices + up to 10 news)

    def _scrape_crypto_fallback(self):
        """Fallback method for crypto scraping without AI Agent"""
        articles = []

        try:
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                'vs_currency': 'usd',
                'order': 'market_cap_desc',
                'per_page': 10,
                'page': 1,
                'sparkline': False,
                'price_change_percentage': '24h'
            }

            response = requests.get(url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()

                for coin in data[:10]:
                    coin_name = coin.get('name', '')
                    symbol = coin.get('symbol', '').upper()
                    usd_price = coin.get('current_price', 0)
                    change_24h = coin.get('price_change_24h', 0)
                    change_percent = coin.get('price_change_percentage_24h', 0)
                    market_cap = coin.get('market_cap', 0)
                    image_url = coin.get('image', '')

                    article_data = {
                        'title': f'{coin_name} ({symbol}) ${usd_price:,.2f}',
                        'content': f'{coin_name} ({symbol}) ราคาปัจจุบัน ${usd_price:,.2f} เปลี่ยนแปลง 24h: {change_24h:+.2f} ({change_percent:+.2f}%) Market Cap: ${market_cap:,.0f}',
                        'url': f'https://www.coingecko.com/en/coins/{coin.get("id", "")}',
                        'price': usd_price,
                        'change': change_24h,
                        'change_percent': change_percent,
                        'image_url': image_url,
                        'published_at': timezone.now(),
                        'category': 'crypto'
                    }

                    articles.append(article_data)

        except Exception as e:
            print(f"Error in fallback crypto scraping: {e}")

        return articles

    def scrape_gold(self):
        """ดึงข้อมูลราคาทองคำ - 10 เว็บ (3 ราคาจาก yfinance + 10 ร้านทอง/เว็บข่าว)"""
        articles = []

        # Part 1: ราคาทองคำจาก yfinance (3 รูปแบบ)
        if YFINANCE_AVAILABLE:
            gold_symbols = [
                ('GC=F', 'Gold Futures (COMEX)', 'https://finance.yahoo.com/quote/GC=F'),
                ('XAUUSD=X', 'Gold Spot (XAU/USD)', 'https://finance.yahoo.com/quote/XAUUSD=X'),
                ('GLD', 'Gold ETF (SPDR)', 'https://finance.yahoo.com/quote/GLD')
            ]

            for symbol, name, url in gold_symbols:
                try:
                    ticker = yf.Ticker(symbol)
                    info = ticker.info
                    history = ticker.history(period='1d')

                    if not history.empty:
                        price = history['Close'].iloc[-1]
                        prev_close = info.get('previousClose', price)
                        change = price - prev_close
                        change_percent = (change / prev_close * 100) if prev_close > 0 else 0

                        articles.append({
                            'title': f'{name} ${price:.2f}',
                            'content': f'{name} ราคา ${price:.2f} เปลี่ยนแปลง {change:+.2f} ({change_percent:+.2f}%)',
                            'url': url,
                            'price': price,
                            'change': change,
                            'change_percent': change_percent,
                            'published_at': timezone.now(),
                            'category': 'gold'
                        })
                        print(f"✓ Scraped {name}: ${price:.2f}")

                except Exception as e:
                    print(f"Error scraping {name}: {e}")

        # Part 2: ข่าวและราคาจาก 10 เว็บไซต์ทอง (ไทย + สากล)
        gold_news_sources = [
            # Thai Gold Shops
            ('https://www.goldtraders.or.th/', '.price-display', 'สมาคมค้าทองคำ'),
            ('https://www.huasengheng.com/gold-price', '.gold-price-item', 'ฮั่วเซ่งเฮง'),
            ('https://www.ylgfutures.co.th/gold-price', '.price-table', 'YLG'),
            ('https://www.finnomena.com/gold', 'article h3 a', 'Finnomena Gold'),
            ('https://www.aurora.co.th/gold-price', '.price-item', 'Aurora'),
            ('https://www.intergold.co.th/gold-price', '.price-display', 'InterGOLD'),
            # International Gold News
            ('https://th.tradingview.com/symbols/XAUUSD/', 'a', 'TradingView XAUUSD'),
            ('https://th.investing.com/currencies/xau-usd', 'article a', 'Investing.com Gold'),
            ('https://www.kitco.com/', 'article h3 a', 'Kitco'),
            ('https://goldprice.org/', '.price-display', 'GoldPrice.org'),
        ]

        for source_url, selector, source_name in gold_news_sources:
            try:
                # Use Thai headers for Thai sites
                headers_local = {**self.headers}
                if '.th' in source_url or 'thai' in source_url.lower():
                    headers_local['Accept-Language'] = 'th-TH,th;q=0.9,en;q=0.8'

                response = requests.get(source_url, headers=headers_local, timeout=10, verify=False)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Try to find price or news
                    elements = soup.select(selector)[:1]

                    for elem in elements:
                        try:
                            if elem.name == 'a':
                                # It's a news link
                                title = elem.text.strip()
                                article_url = elem.get('href', '')

                                if not article_url.startswith('http'):
                                    base_url = source_url.rsplit('/', 2)[0]
                                    article_url = base_url + article_url

                                articles.append({
                                    'title': f'[{source_name}] {title}',
                                    'content': f'ข่าวทองคำจาก {source_name}: {title}',
                                    'url': article_url if article_url else source_url,
                                    'published_at': timezone.now(),
                                    'category': 'gold'
                                })
                            else:
                                # It's a price display
                                price_text = elem.text.strip()
                                articles.append({
                                    'title': f'[{source_name}] {price_text}',
                                    'content': f'ราคาทองคำจาก {source_name}: {price_text}',
                                    'url': source_url,
                                    'published_at': timezone.now(),
                                    'category': 'gold'
                                })

                            print(f"✓ Scraped gold info from {source_name}")

                        except Exception as e:
                            print(f"Error parsing gold info from {source_name}: {e}")
            except Exception as e:
                print(f"Error scraping gold from {source_name}: {e}")

        return articles[:15]  # Top 15 (3 from yfinance + up to 10 from websites)

    def scrape_tech_ai(self):
        """ดึงข้อมูลข่าว AI - เว็บไซต์น่าเชื่อถือ (เก็บเว็บเก่า + เพิ่มใหม่)"""
        articles = []

        sources = [
            # New trusted sources
            ('https://news.mit.edu/topic/artificial-intelligence2', 'h3 a'),
            ('https://ai.stanford.edu/', 'h3 a'),
            ('https://openai.com/blog/', 'h3 a'),
            ('https://ai.google/discover/', 'h3 a'),
            ('https://deepmind.google/blog/', 'h3 a'),
            ('https://ai.meta.com/blog/', 'h3 a'),
            ('https://developer.nvidia.com/', 'h3 a'),
            ('https://towardsdatascience.com/', 'h3 a'),
            ('https://www.kdnuggets.com/', 'h3 a'),
            ('https://www.analyticsvidhya.com/', 'h3 a'),
            # Keep old sources
            ('https://techcrunch.com/category/artificial-intelligence/', 'article h2 a'),
            ('https://www.theverge.com/ai-artificial-intelligence', '.duet--article--title-segment a'),
            ('https://www.artificialintelligence-news.com/', 'h3.entry-title a'),
            ('https://venturebeat.com/category/ai/', 'h2.article-title a'),
            ('https://www.technologyreview.com/topic/artificial-intelligence/', 'h3 a'),
            ('https://www.wired.com/tag/artificial-intelligence/', 'h3 a'),
            ('https://www.forbes.com/ai/', 'article h3 a'),
            ('https://ai.googleblog.com/', '.post-title a')
        ]

        for source_url, selector in sources:
            try:
                response = requests.get(source_url, headers=self.headers, timeout=10, verify=False)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_links = soup.select(selector)[:5]  # 5 ข่าวต่อเว็บ = 50 เว็บ

                    for link in article_links:
                        try:
                            title = link.text.strip()
                            article_url = link.get('href', '')

                            if not article_url.startswith('http'):
                                base_url = source_url.rstrip('/').split('/category')[0].split('/tag')[0].split('/topic')[0]
                                article_url = base_url + article_url

                            article_data = {
                                'title': title,
                                'content': f'ข่าว AI: {title}',
                                'url': article_url,
                                'published_at': timezone.now(),
                                'category': 'tech_ai'
                            }

                            articles.append(article_data)
                            print(f"✓ Scraped AI news from {source_url}")

                        except Exception as e:
                            print(f"Error parsing AI article: {e}")

            except Exception as e:
                print(f"Error scraping AI news from {source_url}: {e}")

        return articles[:10]

    def scrape_tech_hardware(self):
        """ดึงข้อมูลข่าว Hardware - เว็บไซต์น่าเชื่อถือ (เก็บเว็บเก่า + เพิ่มใหม่)"""
        articles = []

        sources = [
            # New trusted sources
            ('https://www.tomshardware.com/', 'article h3 a'),
            ('https://www.techspot.com/', 'h3 a'),
            ('https://www.anandtech.com/', '.article-title a'),
            ('https://www.pcmag.com/', 'h3 a'),
            ('https://www.kitguru.net/', 'h3 a'),
            ('https://wccftech.com/', 'h3 a'),
            ('https://www.techpowerup.com/', '.newslink a'),
            # Keep old sources
            ('https://www.pcgamer.com/hardware/', 'h3 a'),
            ('https://www.guru3d.com/news/', 'h3 a'),
            ('https://www.overclock3d.net/', 'h3 a'),
            ('https://www.hardwareluxx.com/', 'h3 a'),
            ('https://hexus.net/', '.headline a'),
            ('https://www.tweaktown.com/news/', 'h3 a')
        ]

        for source_url, selector in sources:
            try:
                response = requests.get(source_url, headers=self.headers, timeout=10, verify=False)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_links = soup.select(selector)[:5]  # 5 ข่าวต่อเว็บ = 50 เว็บ

                    for link in article_links:
                        try:
                            title = link.text.strip()
                            article_url = link.get('href', '')

                            if not article_url.startswith('http'):
                                base_url = source_url.rstrip('/')
                                article_url = base_url + article_url

                            article_data = {
                                'title': title,
                                'content': f'ข่าว Hardware: {title}',
                                'url': article_url,
                                'published_at': timezone.now(),
                                'category': 'tech_hardware'
                            }

                            articles.append(article_data)
                            print(f"✓ Scraped Hardware news from {source_url}")

                        except Exception as e:
                            print(f"Error parsing hardware article: {e}")

            except Exception as e:
                print(f"Error scraping hardware news from {source_url}: {e}")

        return articles[:10]

    def scrape_tech_software(self):
        """ดึงข้อมูลข่าว Software - เว็บไซต์น่าเชื่อถือ (เก็บเว็บเก่า + เพิ่มใหม่)"""
        articles = []

        sources = [
            # New trusted sources
            ('https://github.com/trending', 'h2 a'),
            ('https://stackoverflow.com/questions', 'h3 a'),
            ('https://dev.to/', 'h3 a'),
            ('https://hashnode.com/', 'h3 a'),
            ('https://www.g2.com/categories/software-development', 'h3 a'),
            ('https://www.capterra.com/', 'h3 a'),
            ('https://www.trustradius.com/', 'h3 a'),
            ('https://www.cnet.com/tech/services-and-software/', 'h3 a'),
            # Keep old sources
            ('https://www.zdnet.com/topic/software/', 'article h3 a'),
            ('https://www.infoworld.com/software/', 'h3 a'),
            ('https://www.computerworld.com/category/software/', 'h3 a'),
            ('https://www.theregister.com/software/', 'h4 a'),
            ('https://www.eweek.com/software/', 'h3 a'),
            ('https://www.softwaretestingnews.co.uk/', 'h3 a'),
            ('https://devclass.com/', 'h3 a'),
            ('https://sdtimes.com/', 'h3 a'),
            ('https://www.developerdrive.com/', 'h3 a'),
            ('https://www.infoq.com/', 'h3 a')
        ]

        for source_url, selector in sources:
            try:
                response = requests.get(source_url, headers=self.headers, timeout=10, verify=False)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_links = soup.select(selector)[:5]  # 5 ข่าวต่อเว็บ = 50 เว็บ

                    for link in article_links:
                        try:
                            title = link.text.strip()
                            article_url = link.get('href', '')

                            if not article_url.startswith('http'):
                                base_url = source_url.rstrip('/').split('/topic')[0].split('/category')[0]
                                article_url = base_url + article_url

                            article_data = {
                                'title': title,
                                'content': f'ข่าว Software: {title}',
                                'url': article_url,
                                'published_at': timezone.now(),
                                'category': 'tech_software'
                            }

                            articles.append(article_data)
                            print(f"✓ Scraped Software news from {source_url}")

                        except Exception as e:
                            print(f"Error parsing software article: {e}")

            except Exception as e:
                print(f"Error scraping software news from {source_url}: {e}")

        return articles[:10]

    def scrape_football_news(self):
        """ดึงข้อมูลข่าว Football - เว็บไซต์น่าเชื่อถือ (เก็บเว็บเก่า + เพิ่มใหม่)"""
        articles = []

        sources = [
            # New trusted sources
            ('https://www.livescore.com/en/', 'h3 a'),
            ('https://www.espn.com/soccer/', '.contentItem__title a'),
            ('https://www.skysports.com/football', 'h3 a'),
            ('https://www.bbc.com/sport/football', 'h3 a'),
            ('https://www.goal.com/en', 'h3 a'),
            ('https://www.premierleague.com/news', 'h3 a'),
            ('https://www.uefa.com/news/', 'h3 a'),
            ('https://www.laliga.com/en-GB/news', 'h3 a'),
            ('https://www.legaseriea.it/en/news', 'h3 a'),
            ('https://www.bundesliga.com/en/bundesliga/news', 'h3 a'),
            # Keep old sources
            ('https://www.theguardian.com/football', 'h3 a'),
            ('https://www.fourfourtwo.com/news', 'h3 a'),
            ('https://www.transfermarkt.com/', 'h3 a'),
            ('https://www.90min.com/', 'h3 a'),
            ('https://onefootball.com/en', 'h3 a')
        ]

        for source_url, selector in sources:
            try:
                response = requests.get(source_url, headers=self.headers, timeout=10, verify=False)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_links = soup.select(selector)[:5]  # 5 ข่าวต่อเว็บ = 50 เว็บ

                    for link in article_links:
                        try:
                            title = link.text.strip()
                            article_url = link.get('href', '')

                            if not article_url.startswith('http'):
                                base_url = source_url.rstrip('/')
                                article_url = base_url + article_url

                            article_data = {
                                'title': title,
                                'content': f'ข่าวฟุตบอล: {title}',
                                'url': article_url,
                                'published_at': timezone.now(),
                                'category': 'football'
                            }

                            articles.append(article_data)
                            print(f"✓ Scraped Football news from {source_url}")

                        except Exception as e:
                            print(f"Error parsing football article: {e}")

            except Exception as e:
                print(f"Error scraping football news from {source_url}: {e}")

        return articles[:10]

    def scrape_ev_car_news(self):
        """ดึงข้อมูลข่าว EV Car - เว็บไซต์น่าเชื่อถือ (เก็บเว็บเก่า + เพิ่มใหม่)"""
        articles = []

        sources = [
            # New trusted sources
            ('https://insideevs.com/', 'h3 a'),
            ('https://thedriven.io/', 'h3 a'),
            ('https://electrek.co/', '.article-title a'),
            ('https://evmagazine.com/', 'h3 a'),
            # Keep old sources
            ('https://www.notateslaapp.com/', 'h3 a'),
            ('https://cleantechnica.com/', 'h3 a'),
            ('https://www.greencarreports.com/', 'h3 a'),
            ('https://www.evannex.com/blogs/news', 'h3 a'),
            ('https://electrive.com/', 'h3 a'),
            ('https://www.teslarati.com/', 'h3 a'),
            ('https://www.caranddriver.com/news/electric-cars/', 'h3 a'),
            ('https://www.motortrend.com/features/electric-vehicles/', 'h3 a')
        ]

        for source_url, selector in sources:
            try:
                response = requests.get(source_url, headers=self.headers, timeout=10, verify=False)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_links = soup.select(selector)[:5]  # 5 ข่าวต่อเว็บ = 50 เว็บ

                    for link in article_links:
                        try:
                            title = link.text.strip()
                            article_url = link.get('href', '')

                            if not article_url.startswith('http'):
                                base_url = source_url.rstrip('/')
                                article_url = base_url + article_url

                            article_data = {
                                'title': title,
                                'content': f'ข่าว EV Car: {title}',
                                'url': article_url,
                                'published_at': timezone.now(),
                                'category': 'ev_car'
                            }

                            articles.append(article_data)
                            print(f"✓ Scraped EV Car news from {source_url}")

                        except Exception as e:
                            print(f"Error parsing EV car article: {e}")

            except Exception as e:
                print(f"Error scraping EV car news from {source_url}: {e}")

        return articles[:10]

    def scrape_rocket_space_news(self):
        """ดึงข้อมูลข่าว Rocket & Space - เว็บไซต์น่าเชื่อถือ (เก็บเว็บเก่า + เพิ่มใหม่)"""
        articles = []

        sources = [
            # New trusted sources
            ('https://www.nasa.gov/news/', 'h3 a'),
            ('https://www.esa.int/Newsroom', 'h3 a'),
            ('https://www.spacex.com/updates/', 'h3 a'),
            ('https://spaceflightnow.com/', 'h3 a'),
            ('https://nasaspaceflight.com/', 'h3 a'),
            ('https://www.space.com/news', 'article h3 a'),
            ('https://www.planetary.org/articles', 'h3 a'),
            # Keep old sources
            ('https://spacenews.com/', '.c-title__link a'),
            ('https://arstechnica.com/space/', 'h3 a'),
            ('https://www.universetoday.com/', 'h3 a'),
            ('https://www.blueorigin.com/news', 'h3 a')
        ]

        for source_url, selector in sources:
            try:
                response = requests.get(source_url, headers=self.headers, timeout=10, verify=False)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_links = soup.select(selector)[:5]  # 5 ข่าวต่อเว็บ = 50 เว็บ

                    for link in article_links:
                        try:
                            title = link.text.strip()
                            article_url = link.get('href', '')

                            if not article_url.startswith('http'):
                                if source_url.endswith('/news') or source_url.endswith('/news/'):
                                    base_url = source_url.rsplit('/news', 1)[0]
                                else:
                                    base_url = source_url.rstrip('/')
                                article_url = base_url + article_url

                            article_data = {
                                'title': title,
                                'content': f'ข่าว Rocket & Space: {title}',
                                'url': article_url,
                                'published_at': timezone.now(),
                                'category': 'rocket_space'
                            }

                            articles.append(article_data)
                            print(f"✓ Scraped Rocket/Space news from {source_url}")

                        except Exception as e:
                            print(f"Error parsing rocket/space article: {e}")

            except Exception as e:
                print(f"Error scraping rocket/space news from {source_url}: {e}")

        return articles[:10]

    def scrape_ecommerce_deals(self):
        """ดึงข้อมูล E-Commerce Deals - Lazada, Shopee, Taobao, Tmall, Pinduoduo, Alibaba, Amazon, TikTok"""
        articles = []

        print("🛒 Starting E-Commerce price scraping...")

        # Southeast Asia Platforms
        articles.extend(self._scrape_lazada())
        articles.extend(self._scrape_shopee())
        articles.extend(self._scrape_tiktok_shop())

        # China Platforms
        articles.extend(self._scrape_taobao())
        articles.extend(self._scrape_tmall())
        articles.extend(self._scrape_pinduoduo())
        articles.extend(self._scrape_1688())

        # International Platforms
        articles.extend(self._scrape_alibaba())
        articles.extend(self._scrape_amazon())

        print(f"✓ E-Commerce scraping completed: {len(articles)} products found")
        return articles[:20]  # Top 20 deals across all platforms

    def _scrape_lazada(self):
        """Scrape Lazada Thailand - Flash Sale & Best Sellers"""
        products = []
        sources = [
            ('https://www.lazada.co.th/shop-flash-sale/', 'Flash Sale'),
            ('https://www.lazada.co.th/best-sellers/', 'Best Sellers'),
        ]

        for url, category in sources:
            try:
                response = requests.get(url, headers=self.headers, timeout=15, verify=False)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Lazada uses dynamic loading, try multiple selectors
                    product_items = soup.select('[data-qa-locator="product-item"]')[:2]

                    for item in product_items:
                        try:
                            title_elem = item.select_one('.title, [data-qa-locator="product-name"]')
                            price_elem = item.select_one('.price, [data-qa-locator="product-price"]')
                            link_elem = item.select_one('a')

                            if title_elem and link_elem:
                                title = title_elem.text.strip()
                                product_url = link_elem.get('href', '')

                                if not product_url.startswith('http'):
                                    product_url = 'https://www.lazada.co.th' + product_url

                                price = None
                                if price_elem:
                                    price_text = price_elem.text.strip().replace('฿', '').replace(',', '').replace(' ', '')
                                    try:
                                        price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                                    except:
                                        pass

                                products.append({
                                    'title': f'[Lazada {category}] {title[:100]}',
                                    'content': f'Lazada Thailand - {category}: {title}',
                                    'url': product_url,
                                    'price': price,
                                    'published_at': timezone.now(),
                                    'category': 'e_commerce'
                                })
                                print(f"✓ Lazada: {title[:50]}...")
                        except Exception as e:
                            print(f"Error parsing Lazada product: {e}")
            except Exception as e:
                print(f"Error scraping Lazada {category}: {e}")

        return products

    def _scrape_shopee(self):
        """Scrape Shopee Thailand - Flash Sale & Trending"""
        products = []
        sources = [
            ('https://shopee.co.th/flash_sale', 'Flash Sale'),
            ('https://shopee.co.th/search?order=desc&sortBy=sales', 'Best Selling'),
        ]

        for url, category in sources:
            try:
                response = requests.get(url, headers=self.headers, timeout=15, verify=False)
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Shopee uses dynamic content, try API-like selectors
                    product_items = soup.select('[data-sqe="item"]')[:2]

                    for item in product_items:
                        try:
                            title_elem = item.select_one('[data-sqe="name"], .shopee-item-card__text-name')
                            price_elem = item.select_one('[data-sqe="price"], .shopee-item-card__current-price')
                            link_elem = item.select_one('a')

                            if title_elem and link_elem:
                                title = title_elem.text.strip()
                                product_url = link_elem.get('href', '')

                                if not product_url.startswith('http'):
                                    product_url = 'https://shopee.co.th' + product_url

                                price = None
                                if price_elem:
                                    price_text = price_elem.text.strip().replace('฿', '').replace(',', '').replace(' ', '')
                                    try:
                                        price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                                    except:
                                        pass

                                products.append({
                                    'title': f'[Shopee {category}] {title[:100]}',
                                    'content': f'Shopee Thailand - {category}: {title}',
                                    'url': product_url,
                                    'price': price,
                                    'published_at': timezone.now(),
                                    'category': 'e_commerce'
                                })
                                print(f"✓ Shopee: {title[:50]}...")
                        except Exception as e:
                            print(f"Error parsing Shopee product: {e}")
            except Exception as e:
                print(f"Error scraping Shopee {category}: {e}")

        return products

    def _scrape_tiktok_shop(self):
        """Scrape TikTok Shop - Popular Products & Trending"""
        products = []
        sources = [
            ('https://shop.tiktok.com/view/discover', 'Trending'),
            ('https://www.tiktok.com/business/th/shop', 'TH Business'),
        ]

        for url, category in sources:
            try:
                # TikTok Shop requires specific headers
                tiktok_headers = {
                    **self.headers,
                    'Accept-Language': 'th-TH,th;q=0.9,en-US;q=0.8,en;q=0.7',
                }

                response = requests.get(url, headers=tiktok_headers, timeout=15, verify=False)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Try multiple selectors for TikTok Shop
                    product_items = soup.select('[data-e2e="search-card-item"], .product-card, [data-product-id]')[:2]

                    for item in product_items:
                        try:
                            title_elem = item.select_one('.title, [data-e2e="search-card-title"], .product-title, h3')
                            price_elem = item.select_one('.price, [data-e2e="search-card-price"], .product-price, .sale-price')
                            link_elem = item.select_one('a')

                            if title_elem and link_elem:
                                title = title_elem.text.strip()
                                product_url = link_elem.get('href', '')

                                if not product_url.startswith('http'):
                                    if 'tiktok.com' in url:
                                        product_url = 'https://www.tiktok.com' + product_url
                                    else:
                                        product_url = 'https://shop.tiktok.com' + product_url

                                price = None
                                if price_elem:
                                    price_text = price_elem.text.strip().replace('$', '').replace('฿', '').replace(',', '').replace(' ', '')
                                    try:
                                        price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                                    except:
                                        pass

                                products.append({
                                    'title': f'[TikTok Shop {category}] {title[:100]}',
                                    'content': f'TikTok Shop - {category}: {title}',
                                    'url': product_url if product_url else url,
                                    'price': price,
                                    'published_at': timezone.now(),
                                    'category': 'e_commerce'
                                })
                                print(f"✓ TikTok Shop {category}: {title[:50]}...")
                        except Exception as e:
                            print(f"Error parsing TikTok Shop product: {e}")
            except Exception as e:
                print(f"Error scraping TikTok Shop {category}: {e}")

        return products

    def _scrape_taobao(self):
        """Scrape Taobao - Hot Items (淘宝)"""
        products = []
        try:
            url = 'https://s.taobao.com/search?q=热卖&sort=sale-desc'
            headers_cn = {**self.headers, 'Accept-Language': 'zh-CN,zh;q=0.9'}

            response = requests.get(url, headers=headers_cn, timeout=15, verify=False)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                product_items = soup.select('.item, .product, [data-category="item"]')[:2]

                for item in product_items:
                    try:
                        title_elem = item.select_one('.title, .item-title, [data-title]')
                        price_elem = item.select_one('.price, .sale-price, strong')
                        link_elem = item.select_one('a')

                        if title_elem and link_elem:
                            title = title_elem.text.strip()
                            product_url = link_elem.get('href', '')

                            if product_url and not product_url.startswith('http'):
                                product_url = 'https:' + product_url if product_url.startswith('//') else product_url

                            price = None
                            if price_elem:
                                price_text = price_elem.text.strip().replace('¥', '').replace(',', '').replace(' ', '')
                                try:
                                    price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                                except:
                                    pass

                            products.append({
                                'title': f'[Taobao] {title[:100]}',
                                'content': f'Taobao Hot Items: {title}',
                                'url': product_url if product_url else 'https://www.taobao.com',
                                'price': price,
                                'published_at': timezone.now(),
                                'category': 'e_commerce'
                            })
                            print(f"✓ Taobao: {title[:50]}...")
                    except Exception as e:
                        print(f"Error parsing Taobao product: {e}")
        except Exception as e:
            print(f"Error scraping Taobao: {e}")

        return products

    def _scrape_tmall(self):
        """Scrape Tmall - Featured Products (天猫)"""
        products = []
        try:
            url = 'https://www.tmall.com'
            headers_cn = {**self.headers, 'Accept-Language': 'zh-CN,zh;q=0.9'}

            response = requests.get(url, headers=headers_cn, timeout=15, verify=False)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                product_items = soup.select('.product, .item, [data-spm="product"]')[:2]

                for item in product_items:
                    try:
                        title_elem = item.select_one('.product-title, .title, h3')
                        price_elem = item.select_one('.price, .product-price, strong')
                        link_elem = item.select_one('a')

                        if title_elem and link_elem:
                            title = title_elem.text.strip()
                            product_url = link_elem.get('href', '')

                            if product_url and not product_url.startswith('http'):
                                product_url = 'https:' + product_url if product_url.startswith('//') else product_url

                            price = None
                            if price_elem:
                                price_text = price_elem.text.strip().replace('¥', '').replace(',', '').replace(' ', '')
                                try:
                                    price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                                except:
                                    pass

                            products.append({
                                'title': f'[Tmall] {title[:100]}',
                                'content': f'Tmall Featured: {title}',
                                'url': product_url if product_url else 'https://www.tmall.com',
                                'price': price,
                                'published_at': timezone.now(),
                                'category': 'e_commerce'
                            })
                            print(f"✓ Tmall: {title[:50]}...")
                    except Exception as e:
                        print(f"Error parsing Tmall product: {e}")
        except Exception as e:
            print(f"Error scraping Tmall: {e}")

        return products

    def _scrape_pinduoduo(self):
        """Scrape Pinduoduo - Group Buy Deals (拼多多)"""
        products = []
        try:
            url = 'https://mobile.yangkeduo.com'
            headers_cn = {**self.headers, 'Accept-Language': 'zh-CN,zh;q=0.9'}

            response = requests.get(url, headers=headers_cn, timeout=15, verify=False)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                product_items = soup.select('.goods-item, [data-goods]')[:2]

                for item in product_items:
                    try:
                        title_elem = item.select_one('.goods-name, .title')
                        price_elem = item.select_one('.price-num, .group-price')
                        link_elem = item.select_one('a')

                        if title_elem and link_elem:
                            title = title_elem.text.strip()
                            product_url = link_elem.get('href', '')

                            if product_url and not product_url.startswith('http'):
                                product_url = 'https://mobile.yangkeduo.com' + product_url

                            price = None
                            if price_elem:
                                price_text = price_elem.text.strip().replace('¥', '').replace(',', '').replace(' ', '')
                                try:
                                    price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                                except:
                                    pass

                            products.append({
                                'title': f'[Pinduoduo] {title[:100]}',
                                'content': f'Pinduoduo Group Buy: {title}',
                                'url': product_url if product_url else 'https://www.pinduoduo.com',
                                'price': price,
                                'published_at': timezone.now(),
                                'category': 'e_commerce'
                            })
                            print(f"✓ Pinduoduo: {title[:50]}...")
                    except Exception as e:
                        print(f"Error parsing Pinduoduo product: {e}")
        except Exception as e:
            print(f"Error scraping Pinduoduo: {e}")

        return products

    def _scrape_1688(self):
        """Scrape 1688.com - Wholesale Deals (阿里巴巴中国站)"""
        products = []
        try:
            url = 'https://www.1688.com/huo/hot.html'
            headers_cn = {**self.headers, 'Accept-Language': 'zh-CN,zh;q=0.9'}

            response = requests.get(url, headers=headers_cn, timeout=15, verify=False)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                product_items = soup.select('.offer-item, [data-offer]')[:2]

                for item in product_items:
                    try:
                        title_elem = item.select_one('.title, .offer-title')
                        price_elem = item.select_one('.price, .moq-price')
                        link_elem = item.select_one('a')

                        if title_elem and link_elem:
                            title = title_elem.text.strip()
                            product_url = link_elem.get('href', '')

                            if product_url and not product_url.startswith('http'):
                                product_url = 'https:' + product_url if product_url.startswith('//') else product_url

                            price = None
                            if price_elem:
                                price_text = price_elem.text.strip().replace('¥', '').replace(',', '').replace(' ', '')
                                try:
                                    price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                                except:
                                    pass

                            products.append({
                                'title': f'[1688] {title[:100]}',
                                'content': f'1688 Wholesale: {title}',
                                'url': product_url if product_url else 'https://www.1688.com',
                                'price': price,
                                'published_at': timezone.now(),
                                'category': 'e_commerce'
                            })
                            print(f"✓ 1688: {title[:50]}...")
                    except Exception as e:
                        print(f"Error parsing 1688 product: {e}")
        except Exception as e:
            print(f"Error scraping 1688: {e}")

        return products

    def _scrape_alibaba(self):
        """Scrape Alibaba.com - B2B Trending Products"""
        products = []
        try:
            url = 'https://www.alibaba.com/trade/search?SearchText=trending'
            response = requests.get(url, headers=self.headers, timeout=15, verify=False)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')

                product_items = soup.select('[data-content="productList"] .organic-list-offer, .product-item')[:2]

                for item in product_items:
                    try:
                        title_elem = item.select_one('.organic-list-offer-title, .title, h2')
                        price_elem = item.select_one('.organic-list-offer-price, .price')
                        link_elem = item.select_one('a.organic-list-offer-outter, a.title')

                        if title_elem and link_elem:
                            title = title_elem.text.strip()
                            product_url = link_elem.get('href', '')

                            if product_url and not product_url.startswith('http'):
                                product_url = 'https://www.alibaba.com' + product_url

                            price = None
                            if price_elem:
                                price_text = price_elem.text.strip().replace('$', '').replace('US', '').replace(',', '').replace(' ', '')
                                try:
                                    # Extract first number (minimum price in range)
                                    price_parts = ''.join(filter(lambda x: x.isdigit() or x == '.' or x == '-', price_text))
                                    if '-' in price_parts:
                                        price = float(price_parts.split('-')[0])
                                    else:
                                        price = float(price_parts) if price_parts else None
                                except:
                                    pass

                            products.append({
                                'title': f'[Alibaba B2B] {title[:100]}',
                                'content': f'Alibaba.com Trending: {title}',
                                'url': product_url if product_url else 'https://www.alibaba.com',
                                'price': price,
                                'published_at': timezone.now(),
                                'category': 'e_commerce'
                            })
                            print(f"✓ Alibaba: {title[:50]}...")
                    except Exception as e:
                        print(f"Error parsing Alibaba product: {e}")
        except Exception as e:
            print(f"Error scraping Alibaba: {e}")

        return products

    def _scrape_amazon(self):
        """Scrape Amazon - Today's Deals & Best Sellers"""
        products = []
        sources = [
            ('https://www.amazon.com/gp/goldbox/', 'Todays Deals'),
            ('https://www.amazon.com/Best-Sellers/zgbs', 'Best Sellers'),
        ]

        for url, category in sources:
            try:
                # Amazon requires more sophisticated headers
                amazon_headers = {
                    **self.headers,
                    'Accept-Language': 'en-US,en;q=0.9',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }

                response = requests.get(url, headers=amazon_headers, timeout=15, verify=False)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')

                    # Amazon uses multiple layouts
                    product_items = soup.select('[data-asin]:not([data-asin=""]), .s-result-item[data-asin]')[:2]

                    for item in product_items:
                        try:
                            title_elem = item.select_one('h2 a span, .a-text-normal, [data-component-type="s-product-image"] + div h2')
                            price_elem = item.select_one('.a-price .a-offscreen, .a-price-whole')
                            link_elem = item.select_one('h2 a, .a-link-normal[href*="/dp/"]')

                            if title_elem and link_elem:
                                title = title_elem.text.strip()
                                product_url = link_elem.get('href', '')

                                if product_url and not product_url.startswith('http'):
                                    product_url = 'https://www.amazon.com' + product_url

                                price = None
                                if price_elem:
                                    price_text = price_elem.text.strip().replace('$', '').replace(',', '').replace(' ', '')
                                    try:
                                        price = float(''.join(filter(lambda x: x.isdigit() or x == '.', price_text)))
                                    except:
                                        pass

                                products.append({
                                    'title': f'[Amazon {category}] {title[:100]}',
                                    'content': f'Amazon {category}: {title}',
                                    'url': product_url if product_url else url,
                                    'price': price,
                                    'published_at': timezone.now(),
                                    'category': 'e_commerce'
                                })
                                print(f"✓ Amazon: {title[:50]}...")
                        except Exception as e:
                            print(f"Error parsing Amazon product: {e}")
            except Exception as e:
                print(f"Error scraping Amazon {category}: {e}")

        return products

    def save_articles(self, articles_by_category):
        """บันทึกบทความลงฐานข้อมูล - ลบข้อมูลเก่าทั้งหมดและสร้างใหม่เสมอ"""
        saved_articles = []
        deleted_count = 0
        created_count = 0

        # ลบข้อมูลเก่าทั้งหมดก่อนสร้างใหม่ (เพื่อหลีกเลี่ยง slug ซ้ำและให้ข้อมูลเป็นปัจจุบันเสมอ)
        print("🗑️  Deleting ALL old articles before inserting fresh data...")
        deleted_count = NewsArticle.objects.all().count()
        NewsArticle.objects.all().delete()
        print(f"✓ Deleted {deleted_count} old articles (all categories cleared)")

        for category, articles in articles_by_category.items():
            for article_data in articles:
                try:
                    # หาหรือสร้าง NewsSource
                    source, _ = NewsSource.objects.get_or_create(
                        name=f"Auto Source - {category}",
                        category=article_data.get('category', category),
                        defaults={
                            'url': article_data['url'],
                            'is_active': True
                        }
                    )

                    # สร้าง article ใหม่เสมอ (ไม่ใช้ get_or_create เพื่อหลีกเลี่ยงการ update เก่า)
                    article = NewsArticle.objects.create(
                        source=source,
                        title=article_data['title'],
                        content=article_data['content'],
                        url=article_data['url'],
                        price=article_data.get('price'),
                        change=article_data.get('change'),
                        change_percent=article_data.get('change_percent'),
                        image_url=article_data.get('image_url'),
                        published_at=article_data['published_at'],
                        scraped_at=timezone.now()
                    )

                    created_count += 1
                    saved_articles.append(article)

                except Exception as e:
                    print(f"Error saving article: {e}")

        print(f"📊 Summary: Deleted {deleted_count}, Created {created_count} new articles")
        return saved_articles


# ========== Standalone Functions ==========


def scrape_all_news_sources():
    """
    Standalone function to scrape all news sources
    Used by views and tasks
    """
    scraper = NewsScraperService()

    # ดึงข้อมูลทุกหมวด
    articles_by_category = scraper.scrape_all_categories()

    # บันทึกลงฐานข้อมูล
    saved_articles = scraper.save_articles(articles_by_category)

    return {
        'total_scraped': sum(len(articles) for articles in articles_by_category.values()),
        'total_saved': len(saved_articles),
        'categories': list(articles_by_category.keys())
    }
