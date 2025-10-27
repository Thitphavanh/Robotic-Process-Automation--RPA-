# E-Commerce Price Scraper Documentation

## Overview
Comprehensive price scraping system for major e-commerce platforms across Southeast Asia, China, and International markets.

## Supported Platforms

### Southeast Asia
1. **Lazada Thailand** (www.lazada.co.th)
   - Flash Sale deals
   - Best Sellers
   - Currency: THB (฿)

2. **Shopee Thailand** (shopee.co.th)
   - Flash Sale
   - Best Selling products
   - Currency: THB (฿)

3. **TikTok Shop** (shop.tiktok.com)
   - Popular/Trending products
   - Currency: USD ($)

### China
4. **Taobao** (www.taobao.com) - 淘宝
   - Hot selling items
   - Search by keywords
   - Currency: CNY (¥)

5. **Tmall** (www.tmall.com) - 天猫
   - Official brand stores
   - Featured products
   - Currency: CNY (¥)

6. **Pinduoduo** (mobile.yangkeduo.com) - 拼多多
   - Group buying deals
   - Wholesale prices
   - Currency: CNY (¥)

7. **1688.com** (www.1688.com) - 阿里巴巴中国站
   - B2B wholesale marketplace
   - Factory direct pricing
   - Currency: CNY (¥)

### International
8. **Alibaba.com** (www.alibaba.com)
   - B2B international marketplace
   - Trending products
   - Currency: USD ($)

9. **Amazon** (www.amazon.com)
   - Today's Deals
   - Best Sellers
   - Currency: USD ($)

## Features

### Data Extraction
- **Product Title**: Full product name with platform prefix (e.g., `[Lazada Flash Sale] Product Name`)
- **Price**: Automatic price extraction with multi-currency support (THB, USD, CNY)
- **Product URL**: Direct link to product page
- **Platform Tag**: Identifies source platform for easy filtering

### Smart Price Parsing
- Removes currency symbols (฿, $, ¥)
- Handles comma separators (1,299.00 → 1299.00)
- Extracts minimum price from price ranges (e.g., "$10-$20" → 10.00)
- Filters non-numeric characters intelligently

### Error Handling
- Graceful fallback for failed platform scraping
- Individual product error handling (continues if one product fails)
- Timeout protection (15 seconds per request)
- SSL verification disabled for problematic sites

## Usage

### Basic Usage
```python
from rpa_bot.news_scraper import NewsScraperService

# Initialize scraper
scraper = NewsScraperService()

# Scrape all e-commerce platforms
products = scraper.scrape_ecommerce_deals()

# Returns up to 20 products across all platforms
print(f"Found {len(products)} products")
```

### Platform-Specific Scraping
```python
# Scrape individual platforms
lazada_products = scraper._scrape_lazada()
shopee_products = scraper._scrape_shopee()
amazon_products = scraper._scrape_amazon()
taobao_products = scraper._scrape_taobao()
```

### Scheduled Scraping (Celery)
```python
# Automatic scraping with Celery Beat
# Runs as part of scrape_all_news() task

from rpa_bot.tasks import scrape_all_news

# This will scrape all categories including e-commerce
result = scrape_all_news.delay()
```

### API Endpoint
```bash
# Trigger scraping via Django API
curl -X POST http://localhost:8000/api/scrape/
```

## Data Structure

### Product Data Format
```python
{
    'title': '[Lazada Flash Sale] iPhone 15 Pro Max 256GB',
    'content': 'Lazada Thailand - Flash Sale: iPhone 15 Pro Max 256GB',
    'url': 'https://www.lazada.co.th/products/...',
    'price': 35990.00,  # Decimal
    'published_at': datetime.now(),
    'category': 'e_commerce'
}
```

### Database Storage
Data is saved to `NewsArticle` model with:
- `title`: Product name with platform prefix
- `content`: Full description
- `url`: Product link
- `price`: Extracted price (Decimal field, 15 digits, 2 decimals)
- `category`: 'e_commerce'
- `source`: Auto-created NewsSource with platform info

## Platform-Specific Notes

### Lazada
- Uses `data-qa-locator` attributes for reliable extraction
- Flash Sale page updates hourly
- Best Sellers page updates daily

### Shopee
- Dynamic content loading (React/Vue)
- Uses `data-sqe` attributes
- May require multiple selector fallbacks

### Chinese Platforms (Taobao, Tmall, Pinduoduo, 1688)
- Use Chinese language headers (`Accept-Language: zh-CN`)
- Some platforms require Chinese characters in search queries
- Anti-bot protection may block requests occasionally
- Consider using proxies for production use

### Amazon
- Strict anti-scraping measures
- Requires sophisticated headers
- Uses ASIN (Amazon Standard Identification Number) in selectors
- IP rotation recommended for high-volume scraping

### TikTok Shop
- Newer platform with evolving structure
- Uses `data-e2e` attributes
- Live streaming integration

## Best Practices

### 1. Rate Limiting
```python
import time

# Add delay between requests to avoid blocking
time.sleep(2)  # 2 second delay
```

### 2. User Agent Rotation
```python
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
}
```

### 3. Proxy Usage (Recommended for Production)
```python
proxies = {
    'http': 'http://proxy.example.com:8080',
    'https': 'https://proxy.example.com:8080',
}

response = requests.get(url, headers=headers, proxies=proxies)
```

### 4. Error Monitoring
```python
import logging

logger = logging.getLogger(__name__)
logger.info(f"✓ Scraped {platform}: {product_title}")
logger.error(f"Error scraping {platform}: {error}")
```

## Limitations & Considerations

### Technical Limitations
1. **Dynamic Content**: Many platforms use JavaScript rendering
   - Solution: Consider using Selenium/Playwright for complete rendering
   - Current: HTML parsing with BeautifulSoup (static content only)

2. **Anti-Bot Protection**: Platforms may block automated scraping
   - Solution: Use residential proxies, rotate user agents
   - Current: Basic headers, SSL verification disabled

3. **Rate Limiting**: Excessive requests may result in IP bans
   - Solution: Implement request throttling, use proxy rotation
   - Current: Sequential requests with timeout

### Legal Considerations
1. **Terms of Service**: Check each platform's ToS regarding data scraping
2. **Robots.txt**: Respect robots.txt directives
3. **Data Usage**: Use scraped data for personal/research purposes only
4. **API Availability**: Prefer official APIs when available:
   - Lazada Open Platform (open.lazada.com)
   - Shopee Open Platform (open.shopee.com)
   - Amazon Product Advertising API
   - Alibaba Open Platform

### Ethical Scraping
- Don't overload servers with excessive requests
- Add reasonable delays between requests
- Don't scrape personal/private information
- Don't use data for spam or malicious purposes
- Consider using official APIs instead

## Official APIs (Recommended Alternative)

### 1. Lazada Open Platform
```
URL: open.lazada.com
Authentication: OAuth 2.0
Features: Product search, pricing, inventory
```

### 2. Shopee Open Platform
```
URL: open.shopee.com
Authentication: Partner key + Shop authorization
Features: Product listings, orders, logistics
```

### 3. Amazon Product Advertising API
```
URL: affiliate-program.amazon.com
Authentication: API key + Affiliate ID
Features: Product search, pricing, reviews
```

### 4. Alibaba Open Platform
```
URL: open.alibaba.com
Authentication: API key
Features: B2B product search, suppliers
```

## Troubleshooting

### No Products Found
```python
# Check if selectors are still valid
# Platforms frequently update their HTML structure

# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Price Extraction Fails
```python
# Price may be in different format or currency
# Check HTML structure manually:

from bs4 import BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')
price_elements = soup.select('.price')  # Adjust selector
print([elem.text for elem in price_elements])
```

### Connection Errors
```python
# Increase timeout
response = requests.get(url, timeout=30)

# Use proxies to avoid IP blocks
proxies = {'http': 'http://proxy:port'}
response = requests.get(url, proxies=proxies)
```

## Future Enhancements

### Planned Features
1. **Selenium Integration**: Full JavaScript rendering
2. **Proxy Rotation**: Built-in proxy pool management
3. **Price History Tracking**: Store historical price data
4. **Price Alerts**: Notify when prices drop below threshold
5. **Product Reviews**: Scrape ratings and reviews
6. **Image Extraction**: Download product images
7. **Multi-Region Support**:
   - Lazada (SG, MY, PH, VN, ID)
   - Shopee (SG, MY, PH, VN, ID, TW)
   - Amazon (UK, DE, JP, CA, etc.)

### Advanced Features
- **AI Price Prediction**: ML model for price trends
- **Comparison Engine**: Cross-platform price comparison
- **Deal Detection**: Identify best deals automatically
- **Coupon Integration**: Find and apply discount codes
- **Affiliate Link Generation**: Automatic affiliate tracking

## Performance Optimization

### Current Performance
- 9 platforms scraped sequentially
- ~2 products per platform
- Total: ~18-20 products per run
- Duration: ~45-90 seconds (depends on network)

### Optimization Tips
```python
# 1. Parallel scraping with ThreadPoolExecutor
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=5) as executor:
    futures = [
        executor.submit(scraper._scrape_lazada),
        executor.submit(scraper._scrape_shopee),
        # ... other platforms
    ]

    results = [future.result() for future in futures]

# 2. Use async/await for concurrent requests
import aiohttp
import asyncio

async def scrape_async():
    async with aiohttp.ClientSession() as session:
        tasks = [
            scrape_platform(session, 'lazada'),
            scrape_platform(session, 'shopee'),
        ]
        return await asyncio.gather(*tasks)
```

## Support & Contribution

### Reporting Issues
- Check if selectors are outdated
- Verify network connectivity
- Check platform's robots.txt
- Review error logs

### Contributing
To add a new platform:
1. Create `_scrape_platformname()` method
2. Add to `scrape_ecommerce_deals()` orchestrator
3. Test with sample URLs
4. Update documentation
5. Submit pull request

## License & Disclaimer

This scraper is for educational and research purposes only. Users are responsible for:
- Complying with each platform's Terms of Service
- Respecting robots.txt directives
- Avoiding excessive requests that may harm platforms
- Using data ethically and legally

No warranty is provided. Use at your own risk.
