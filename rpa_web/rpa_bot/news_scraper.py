"""
News Scraper Service - ดึงข้อมูลข่าวจากหลายแหล่ง (10 รายการล่าสุดต่อหมวด)
"""
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from django.utils import timezone
from .models import NewsSource, NewsArticle

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

        return results

    def scrape_thai_stocks(self):
        """ดึงข้อมูลหุ้นไทย - 10 บริษัทล่าสุด"""
        articles = []

        # TOP 10 หุ้นไทยที่น่าสนใจ
        thai_stocks = [
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
        ]

        if not YFINANCE_AVAILABLE:
            print("yfinance not available, skipping Thai stocks")
            return articles

        for symbol, name in thai_stocks[:10]:
            try:
                # ใช้ yfinance ดึงข้อมูล
                ticker = yf.Ticker(symbol)
                info = ticker.info
                history = ticker.history(period='1d')

                if not history.empty:
                    price = history['Close'].iloc[-1]

                    # ดึงราคาเมื่อวาน
                    prev_close = info.get('previousClose', price)

                    # คำนวณการเปลี่ยนแปลง
                    change = price - prev_close
                    change_percent = (change / prev_close * 100) if prev_close > 0 else 0

                    url = f"https://finance.yahoo.com/quote/{symbol}"
                    image_url = f"https://logo.clearbit.com/{name.lower().replace(' ', '')}.com"

                    article_data = {
                        'title': f'{name} ({symbol}) ราคา {price:.2f} บาท',
                        'content': f'หุ้น {name} ({symbol}) ราคาปัจจุบัน {price:.2f} บาท เปลี่ยนแปลง {change:+.2f} ({change_percent:+.2f}%)',
                        'url': url,
                        'price': price,
                        'change': change,
                        'change_percent': change_percent,
                        'image_url': image_url,
                        'published_at': timezone.now(),
                        'category': 'stock_thai'
                    }

                    articles.append(article_data)
                    print(f"✓ Scraped {name}: ${price:.2f}")

            except Exception as e:
                print(f"Error scraping {name}: {e}")

        return articles

    def scrape_us_stocks(self):
        """ดึงข้อมูลหุ้นอเมริกา - 10 บริษัทล่าสุด"""
        articles = []

        # TOP 10 หุ้นอเมริกา
        us_stocks = [
            ('AAPL', 'Apple'),
            ('MSFT', 'Microsoft'),
            ('GOOGL', 'Alphabet (Google)'),
            ('AMZN', 'Amazon'),
            ('NVDA', 'NVIDIA'),
            ('TSLA', 'Tesla'),
            ('META', 'Meta (Facebook)'),
            ('BRK-B', 'Berkshire Hathaway'),
            ('JPM', 'JPMorgan Chase'),
            ('V', 'Visa')
        ]

        if not YFINANCE_AVAILABLE:
            print("yfinance not available, skipping US stocks")
            return articles

        for symbol, name in us_stocks[:10]:
            try:
                # ใช้ yfinance ดึงข้อมูล
                ticker = yf.Ticker(symbol)
                info = ticker.info
                history = ticker.history(period='1d')

                if not history.empty:
                    price = history['Close'].iloc[-1]

                    # ดึงราคาเมื่อวาน
                    prev_close = info.get('previousClose', price)

                    # คำนวณการเปลี่ยนแปลง
                    change = price - prev_close
                    change_percent = (change / prev_close * 100) if prev_close > 0 else 0

                    url = f"https://finance.yahoo.com/quote/{symbol}"
                    image_url = f"https://logo.clearbit.com/{name.split()[0].lower()}.com"

                    article_data = {
                        'title': f'{name} ({symbol}) ${price:,.2f}',
                        'content': f'หุ้น {name} ({symbol}) ราคาปัจจุบัน ${price:,.2f} เปลี่ยนแปลง {change:+.2f} ({change_percent:+.2f}%)',
                        'url': url,
                        'price': price,
                        'change': change,
                        'change_percent': change_percent,
                        'image_url': image_url,
                        'published_at': timezone.now(),
                        'category': 'stock_us'
                    }

                    articles.append(article_data)
                    print(f"✓ Scraped {name}: ${price:.2f}")

            except Exception as e:
                print(f"Error scraping {name}: {e}")

        return articles

    def scrape_europe_stocks(self):
        """ดึงข้อมูลหุ้นยุโรป - 10 บริษัทล่าสุด"""
        articles = []

        # TOP 10 หุ้นยุโรป
        europe_stocks = [
            ('MC.PA', 'LVMH (ฝรั่งเศส)'),
            ('ASML.AS', 'ASML (เนเธอร์แลนด์)'),
            ('NVO', 'Novo Nordisk (เดนมาร์ก)'),
            ('SAP', 'SAP (เยอรมนี)'),
            ('OR.PA', "L'Oréal (ฝรั่งเศส)"),
            ('SAN.PA', 'Sanofi (ฝรั่งเศส)'),
            ('SIE.DE', 'Siemens (เยอรมนี)'),
            ('NESN.SW', 'Nestlé (สวิตเซอร์แลนด์)'),
            ('NOVN.SW', 'Novartis (สวิตเซอร์แลนด์)'),
            ('SHEL.L', 'Shell (อังกฤษ)')
        ]

        if not YFINANCE_AVAILABLE:
            print("yfinance not available, skipping Europe stocks")
            return articles

        for symbol, name in europe_stocks[:10]:
            try:
                # ใช้ yfinance ดึงข้อมูล
                ticker = yf.Ticker(symbol)
                info = ticker.info
                history = ticker.history(period='1d')

                if not history.empty:
                    price = history['Close'].iloc[-1]

                    # ดึงราคาเมื่อวาน
                    prev_close = info.get('previousClose', price)

                    # คำนวณการเปลี่ยนแปลง
                    change = price - prev_close
                    change_percent = (change / prev_close * 100) if prev_close > 0 else 0

                    url = f"https://finance.yahoo.com/quote/{symbol}"
                    image_url = f"https://logo.clearbit.com/{name.split()[0].lower()}.com"

                    article_data = {
                        'title': f'{name} ({symbol}) €{price:,.2f}',
                        'content': f'หุ้น {name} ({symbol}) ราคาปัจจุบัน €{price:,.2f} เปลี่ยนแปลง {change:+.2f} ({change_percent:+.2f}%)',
                        'url': url,
                        'price': price,
                        'change': change,
                        'change_percent': change_percent,
                        'image_url': image_url,
                        'published_at': timezone.now(),
                        'category': 'stock_europe'
                    }

                    articles.append(article_data)
                    print(f"✓ Scraped {name}: €{price:.2f}")

            except Exception as e:
                print(f"Error scraping {name}: {e}")

        return articles

    def scrape_china_stocks(self):
        """ดึงข้อมูลหุ้นจีน - 10 บริษัทล่าสุด"""
        articles = []

        # TOP 10 หุ้นจีน
        china_stocks = [
            ('BABA', 'Alibaba'),
            ('TCEHY', 'Tencent'),
            ('JD', 'JD.com'),
            ('BIDU', 'Baidu'),
            ('NIO', 'NIO'),
            ('XPEV', 'XPeng'),
            ('LI', 'Li Auto'),
            ('PDD', 'Pinduoduo'),
            ('NTES', 'NetEase'),
            ('TME', 'Tencent Music')
        ]

        if not YFINANCE_AVAILABLE:
            print("yfinance not available, skipping China stocks")
            return articles

        for symbol, name in china_stocks[:10]:
            try:
                # ใช้ yfinance ดึงข้อมูล
                ticker = yf.Ticker(symbol)
                info = ticker.info
                history = ticker.history(period='1d')

                if not history.empty:
                    price = history['Close'].iloc[-1]

                    # ดึงราคาเมื่อวาน
                    prev_close = info.get('previousClose', price)

                    # คำนวณการเปลี่ยนแปลง
                    change = price - prev_close
                    change_percent = (change / prev_close * 100) if prev_close > 0 else 0

                    url = f"https://finance.yahoo.com/quote/{symbol}"
                    image_url = f"https://logo.clearbit.com/{name.split()[0].lower()}.com"

                    article_data = {
                        'title': f'{name} ({symbol}) ${price:,.2f}',
                        'content': f'หุ้น {name} ({symbol}) ราคาปัจจุบัน ${price:,.2f} เปลี่ยนแปลง {change:+.2f} ({change_percent:+.2f}%)',
                        'url': url,
                        'price': price,
                        'change': change,
                        'change_percent': change_percent,
                        'image_url': image_url,
                        'published_at': timezone.now(),
                        'category': 'stock_china'
                    }

                    articles.append(article_data)
                    print(f"✓ Scraped {name}: ${price:.2f}")

            except Exception as e:
                print(f"Error scraping {name}: {e}")

        return articles

    def scrape_crypto(self):
        """ดึงข้อมูล Cryptocurrency - 10 สกุลล่าสุด"""
        articles = []

        try:
            # ใช้ CoinGecko API (ไม่ต้อง API Key)
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
                    change_24h = coin.get('price_change_24h', 0)  # เปลี่ยนแปลงเป็นตัวเลข
                    change_percent = coin.get('price_change_percentage_24h', 0)
                    market_cap = coin.get('market_cap', 0)
                    image_url = coin.get('image', '')  # รูปภาพจาก CoinGecko

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
            print(f"Error scraping crypto: {e}")

        return articles

    def scrape_gold(self):
        """ดึงข้อมูลราคาทองคำ"""
        articles = []

        if not YFINANCE_AVAILABLE:
            print("yfinance not available, skipping gold")
            return articles

        try:
            # ใช้ yfinance ดึงข้อมูลทองคำ (GC=F = Gold Futures)
            ticker = yf.Ticker("GC=F")
            info = ticker.info
            history = ticker.history(period='1d')

            if not history.empty:
                price = history['Close'].iloc[-1]

                # ดึงราคาเมื่อวาน
                prev_close = info.get('previousClose', price)

                # คำนวณการเปลี่ยนแปลง
                change = price - prev_close
                change_percent = (change / prev_close * 100) if prev_close > 0 else 0

                url = "https://finance.yahoo.com/quote/GC=F"

                article_data = {
                    'title': f'ราคาทองคำ ${price:.2f}/oz',
                    'content': f'ราคาทองคำวันนี้อยู่ที่ ${price:.2f} ต่อออนซ์ เปลี่ยนแปลง {change:+.2f} ({change_percent:+.2f}%)',
                    'url': url,
                    'price': price,
                    'change': change,
                    'change_percent': change_percent,
                    'published_at': timezone.now(),
                    'category': 'gold'
                }

                articles.append(article_data)
                print(f"✓ Scraped Gold: ${price:.2f}/oz")

        except Exception as e:
            print(f"Error scraping gold: {e}")

        return articles

    def scrape_tech_ai(self):
        """ดึงข้อมูลข่าว AI - 10 ข่าวล่าสุด"""
        articles = []

        sources = [
            'https://techcrunch.com/category/artificial-intelligence/',
            'https://www.theverge.com/ai-artificial-intelligence'
        ]

        for source_url in sources:
            try:
                response = requests.get(source_url, headers=self.headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_links = soup.select('article h2 a, .duet--article--title-segment a')[:5]

                    for link in article_links:
                        try:
                            title = link.text.strip()
                            article_url = link.get('href', '')

                            if not article_url.startswith('http'):
                                article_url = source_url.split('/category')[0] + article_url

                            article_data = {
                                'title': title,
                                'content': f'ข่าว AI: {title}',
                                'url': article_url,
                                'published_at': timezone.now(),
                                'category': 'tech_ai'
                            }

                            articles.append(article_data)

                        except Exception as e:
                            print(f"Error parsing AI article: {e}")

            except Exception as e:
                print(f"Error scraping AI news: {e}")

        return articles[:10]

    def scrape_tech_hardware(self):
        """ดึงข้อมูลข่าว Hardware - 10 ข่าวล่าสุด"""
        articles = []

        try:
            url = 'https://www.tomshardware.com/'
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                article_links = soup.select('article h3 a, .article-name a')[:10]

                for link in article_links:
                    try:
                        title = link.text.strip()
                        article_url = link.get('href', '')

                        if not article_url.startswith('http'):
                            article_url = 'https://www.tomshardware.com' + article_url

                        article_data = {
                            'title': title,
                            'content': f'ข่าว Hardware: {title}',
                            'url': article_url,
                            'published_at': timezone.now(),
                            'category': 'tech_hardware'
                        }

                        articles.append(article_data)

                    except Exception as e:
                        print(f"Error parsing hardware article: {e}")

        except Exception as e:
            print(f"Error scraping hardware news: {e}")

        return articles[:10]

    def scrape_tech_software(self):
        """ดึงข้อมูลข่าว Software - 10 ข่าวล่าสุด"""
        articles = []

        try:
            url = 'https://www.zdnet.com/topic/software/'
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                article_links = soup.select('article h3 a, .story__title a')[:10]

                for link in article_links:
                    try:
                        title = link.text.strip()
                        article_url = link.get('href', '')

                        if not article_url.startswith('http'):
                            article_url = 'https://www.zdnet.com' + article_url

                        article_data = {
                            'title': title,
                            'content': f'ข่าว Software: {title}',
                            'url': article_url,
                            'published_at': timezone.now(),
                            'category': 'tech_software'
                        }

                        articles.append(article_data)

                    except Exception as e:
                        print(f"Error parsing software article: {e}")

        except Exception as e:
            print(f"Error scraping software news: {e}")

        return articles[:10]

    def scrape_football_news(self):
        """ดึงข้อมูลข่าว Football - 10 ข่าวล่าสุด"""
        articles = []

        try:
            url = "https://www.espn.com/soccer/"
            response = requests.get(url, headers=self.headers, timeout=10)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                article_links = soup.select('.contentItem__title a')[:10]

                for link in article_links:
                    try:
                        title = link.text.strip()
                        article_url = link.get('href', '')

                        if not article_url.startswith('http'):
                            article_url = 'https://www.espn.com' + article_url

                        article_data = {
                            'title': title,
                            'content': f'ข่าวฟุตบอล: {title}',
                            'url': article_url,
                            'published_at': timezone.now(),
                            'category': 'football'
                        }

                        articles.append(article_data)

                    except Exception as e:
                        print(f"Error parsing football article: {e}")

        except Exception as e:
            print(f"Error scraping football news: {e}")

        return articles[:10]

    def scrape_ev_car_news(self):
        """ดึงข้อมูลข่าว EV Car (รถยนต์ไฟฟ้า) - 10 ข่าวล่าสุด"""
        articles = []

        sources = [
            ('https://electrek.co/', '.article-title a'),
            ('https://insideevs.com/', 'h3.title a')
        ]

        for source_url, selector in sources:
            try:
                response = requests.get(source_url, headers=self.headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_links = soup.select(selector)[:5]

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

                        except Exception as e:
                            print(f"Error parsing EV car article: {e}")

            except Exception as e:
                print(f"Error scraping EV car news from {source_url}: {e}")

        return articles[:10]

    def scrape_rocket_space_news(self):
        """ดึงข้อมูลข่าว Rocket & Space Technology - 10 ข่าวล่าสุด"""
        articles = []

        sources = [
            ('https://www.space.com/news', 'article h3 a'),
            ('https://spacenews.com/', '.c-title__link')
        ]

        for source_url, selector in sources:
            try:
                response = requests.get(source_url, headers=self.headers, timeout=10)

                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    article_links = soup.select(selector)[:5]

                    for link in article_links:
                        try:
                            title = link.text.strip()
                            article_url = link.get('href', '')

                            if not article_url.startswith('http'):
                                if source_url.endswith('/news'):
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

                        except Exception as e:
                            print(f"Error parsing rocket/space article: {e}")

            except Exception as e:
                print(f"Error scraping rocket/space news from {source_url}: {e}")

        return articles[:10]

    def save_articles(self, articles_by_category):
        """บันทึกบทความลงฐานข้อมูล - อัพเดทข้อมูลถ้ามีอยู่แล้ว"""
        saved_articles = []
        updated_count = 0
        created_count = 0

        for category, articles in articles_by_category.items():
            for article_data in articles:
                try:
                    # หาหรือสร้าง NewsSource
                    source, created = NewsSource.objects.get_or_create(
                        name=f"Auto Source - {category}",
                        category=article_data.get('category', category),
                        defaults={
                            'url': article_data['url'],
                            'is_active': True
                        }
                    )

                    # หา article ที่มี URL เดียวกัน
                    article, created = NewsArticle.objects.get_or_create(
                        url=article_data['url'],
                        defaults={
                            'source': source,
                            'title': article_data['title'],
                            'content': article_data['content'],
                            'price': article_data.get('price'),
                            'change': article_data.get('change'),
                            'change_percent': article_data.get('change_percent'),
                            'image_url': article_data.get('image_url'),
                            'published_at': article_data['published_at'],
                            'scraped_at': timezone.now()
                        }
                    )

                    # ถ้าไม่ใช่ record ใหม่ ให้อัพเดทข้อมูล
                    if not created:
                        article.title = article_data['title']
                        article.content = article_data['content']
                        article.price = article_data.get('price')
                        article.change = article_data.get('change')
                        article.change_percent = article_data.get('change_percent')
                        article.image_url = article_data.get('image_url')
                        article.published_at = article_data['published_at']
                        article.scraped_at = timezone.now()
                        article.save()
                        updated_count += 1
                    else:
                        created_count += 1

                    saved_articles.append(article)

                except Exception as e:
                    print(f"Error saving article: {e}")

        print(f"📊 Summary: Created {created_count}, Updated {updated_count} articles")
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
