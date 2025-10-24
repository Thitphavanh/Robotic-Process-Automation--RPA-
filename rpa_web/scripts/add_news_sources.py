import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.dev')
django.setup()

from rpa_bot.models import NewsSource

def add_default_news_sources():
    sources_to_add = [
        # Stocks - Thailand
        {'name': 'SET News', 'category': 'stock_thai', 'url': 'https://www.set.or.th/th/news', 'selector': 'div.news-item'},
        # Stocks - America
        {'name': 'Yahoo Finance US', 'category': 'stock_foreign', 'url': 'https://finance.yahoo.com/topic/stock-market-news/', 'selector': 'li.stream-item'},
        # Stocks - Europe
        {'name': 'Investing.com Europe Stocks', 'category': 'stock_foreign', 'url': 'https://www.investing.com/news/stock-market-news', 'selector': 'div.textDiv'},
        # Stocks - China
        {'name': 'China Daily Business', 'category': 'stock_foreign', 'url': 'https://www.chinadaily.com.cn/business', 'selector': 'div.mb10.art_box'},
        # Crypto
        {'name': 'CoinDesk', 'category': 'crypto', 'url': 'https://www.coindesk.com/markets/price-indices/', 'selector': 'div.live-price-card'},
        # Gold
        {'name': 'Gold Price', 'category': 'gold', 'url': 'https://goldprice.org/', 'selector': 'div.price-box'},
        # Technology AI
        {'name': 'TechCrunch AI', 'category': 'tech_ai', 'url': 'https://techcrunch.com/category/artificial-intelligence/', 'selector': 'div.post-block'},
        # Technology Hardware
        {'name': 'AnandTech', 'category': 'tech_hardware', 'url': 'https://www.anandtech.com/', 'selector': 'div.article-list-item'},
        # Technology Software
        {'name': 'ZDNet Software', 'category': 'tech_software', 'url': 'https://www.zdnet.com/software/', 'selector': 'article.item'},
        # Football
        {'name': 'ESPN FC', 'category': 'football', 'url': 'https://www.espn.com/soccer/', 'selector': 'section.col-three'},
    ]

    for source_data in sources_to_add:
        source, created = NewsSource.objects.get_or_create(
            name=source_data['name'],
            defaults={
                'category': source_data['category'],
                'url': source_data['url'],
                'selector': source_data['selector'],
                'is_active': True,
            }
        )
        if created:
            print(f"Added new news source: {source.name} ({source.category})")
        else:
            print(f"News source already exists: {source.name} ({source.category})")

if __name__ == '__main__':
    add_default_news_sources()
