"""
News Scraper Service - ดึงข้อมูลข่าวจากหลายแหล่ง
"""
import requests
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from django.utils import timezone
from .models import NewsSource, NewsArticle


class NewsScraperService:
    """Service สำหรับดึงข้อมูลข่าว"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

    def scrape_all_categories(self):
                """ดึงข้อมูลข่าวทุกหมวดหมู่จาก NewsSource ที่กำหนดค่าไว้ในฐานข้อมูล"""
                results = {}
                active_sources = NewsSource.objects.filter(is_active=True)
        
                for source in active_sources:
                    print(f"Scraping from source: {source.name} ({source.category})")
                    articles = self._scrape_from_source(source)
                    if source.category not in results:
                        results[source.category] = []
                    results[source.category].extend(articles)
        
                return results
        
            def _scrape_from_source(self, source):
                """Generic method to scrape articles from a given NewsSource object."""
                articles = []
                try:
                    if source.api_endpoint: # Use API if available
                        # This part needs to be implemented based on specific API structures
                        print(f"Attempting to scrape from API: {source.api_endpoint}")
                        # Example: if it's a simple JSON API
                        response = requests.get(source.api_endpoint, headers=self.headers, timeout=10)
                        response.raise_for_status() # Raise an exception for HTTP errors
                        data = response.json()
                        # Placeholder for API parsing logic
                        # This will need to be customized heavily based on the actual API response
                        # For now, just return an empty list
                        print(f"API scraping for {source.name} not fully implemented yet.")
                        return []
                    elif source.url and source.selector: # Use web scraping
                        print(f"Attempting to scrape from URL: {source.url} with selector: {source.selector}")
                        response = requests.get(source.url, headers=self.headers, timeout=10)
                        response.raise_for_status() # Raise an exception for HTTP errors
                        soup = BeautifulSoup(response.content, 'html.parser')
        
                        # This is a generic approach, might need refinement per source
                        elements = soup.select(source.selector)
                        for elem in elements[:10]: # Limit to 10 articles per source
                            title_elem = elem.select_one('h2 a, h3 a, a.title, .headline a') # Common title selectors
                            if title_elem:
                                title = title_elem.text.strip()
                                article_url = title_elem.get('href', '')
                                if not article_url.startswith('http'):
                                    article_url = source.url.rstrip('/') + '/' + article_url.lstrip('/')
        
                                # Basic content extraction (can be improved)
                                content = elem.text.strip()[:500] + "..." # Take first 500 chars
        
                                articles.append({
                                    'title': title,
                                    'content': content,
                                    'url': article_url,
                                    'published_at': timezone.now(), # Placeholder, actual date needs parsing
                                    'category': source.category,
                                    'source_id': source.id # Link to the actual NewsSource
                                })
                    else:
                        print(f"NewsSource {source.name} ({source.category}) has no URL/selector or API endpoint defined.")
        
                except requests.exceptions.RequestException as e:
                    print(f"Network error scraping {source.name}: {e}")
                except Exception as e:
                    print(f"Error scraping {source.name}: {e}")
        
                return articles
        
            # Remove existing individual scraping methods as they will be replaced by _scrape_from_source
            # The following methods will be deleted:
            # scrape_thai_stocks
            # scrape_foreign_stocks
            # scrape_crypto
            # scrape_gold
            # scrape_tech_news
            # scrape_football_news
        
            # The save_articles method will be updated next.
        
            def save_articles(self, articles_by_category):
                """บันทึกบทความลงฐานข้อมูล"""
                saved_articles = []
        
                for category, articles in articles_by_category.items():
                    for article_data in articles:
                        try:
                            # Use the actual NewsSource object if source_id is provided
                            source = None
                            if 'source_id' in article_data:
                                source = NewsSource.objects.get(id=article_data['source_id'])
                            else:
                                # Fallback for articles without a specific source_id (e.g., from old methods)
                                source, created = NewsSource.objects.get_or_create(
                                    name=f"Auto Source - {article_data.get('category', category)}",
                                    category=article_data.get('category', category),
                                    defaults={
                                        'url': article_data['url'], # This might not be accurate for auto-created sources
                                        'is_active': True
                                    }
                                )
        
                            # สร้าง NewsArticle
                            article, created = NewsArticle.objects.get_or_create(
                                url=article_data['url'],
                                defaults={
                                    'source': source,
                                    'title': article_data['title'],
                                    'content': article_data['content'],
                                    'price': article_data.get('price'),
                                    'change': article_data.get('change'),
                                    'change_percent': article_data.get('change_percent'),
                                    'published_at': article_data['published_at']
                                }
                            )
        
                            saved_articles.append(article)
        
                        except Exception as e:
                            print(f"Error saving article: {e}")
        
                return saved_articles
