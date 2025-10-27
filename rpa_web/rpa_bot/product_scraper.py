"""
Product Scraper Service - ดึงข้อมูลสินค้า E-Commerce แบบละเอียด
รองรับ: Lazada, Shopee, TikTok Shop, Taobao, Tmall, Pinduoduo, JD.com, 1688, Alibaba, AliExpress, Amazon
"""
import requests
import re
from bs4 import BeautifulSoup
from decimal import Decimal
from django.utils import timezone
from .models import TrackedProduct, ProductCategory, ProductBrand, PriceHistory
import urllib3

# Disable SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ProductScraperService:
    """Service สำหรับ scrape ข้อมูลสินค้า E-Commerce"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }

    def detect_platform(self, url):
        """ตรวจสอบว่า URL มาจากแพลตฟอร์มไหน"""
        url_lower = url.lower()

        if 'lazada' in url_lower:
            return 'lazada'
        elif 'shopee' in url_lower:
            return 'shopee'
        elif 'tiktok' in url_lower or 'shop.tiktok' in url_lower:
            return 'tiktok'
        elif 'taobao' in url_lower:
            return 'taobao'
        elif 'tmall' in url_lower:
            return 'tmall'
        elif 'pinduoduo' in url_lower or 'yangkeduo' in url_lower:
            return 'pinduoduo'
        elif 'jd.com' in url_lower or 'jd.hk' in url_lower:
            return 'jd'
        elif '1688' in url_lower:
            return '1688'
        elif 'aliexpress' in url_lower:
            return 'aliexpress'
        elif 'alibaba.com' in url_lower:
            return 'alibaba'
        elif 'amazon' in url_lower:
            return 'amazon'
        else:
            return None

    def scrape_product_by_url(self, product_url):
        """Scrape สินค้าจาก URL"""
        platform = self.detect_platform(product_url)

        if not platform:
            raise ValueError(f"ไม่สามารถระบุแพลตฟอร์มจาก URL: {product_url}")

        # เรียก method ตามแพลตฟอร์ม
        scraper_methods = {
            'lazada': self._scrape_lazada_product,
            'shopee': self._scrape_shopee_product,
            'tiktok': self._scrape_tiktok_product,
            'taobao': self._scrape_taobao_product,
            'tmall': self._scrape_tmall_product,
            'pinduoduo': self._scrape_pinduoduo_product,
            'jd': self._scrape_jd_product,
            '1688': self._scrape_1688_product,
            'alibaba': self._scrape_alibaba_product,
            'aliexpress': self._scrape_aliexpress_product,
            'amazon': self._scrape_amazon_product,
        }

        scraper_method = scraper_methods.get(platform)
        if scraper_method:
            return scraper_method(product_url)
        else:
            raise ValueError(f"ไม่รองรับแพลตฟอร์ม: {platform}")

    def _extract_price(self, price_text):
        """แปลงข้อความราคาเป็นตัวเลข"""
        if not price_text:
            return None

        # Remove currency symbols and common text
        price_text = price_text.replace('฿', '').replace('$', '').replace('¥', '')
        price_text = price_text.replace('THB', '').replace('USD', '').replace('CNY', '')
        price_text = price_text.replace(',', '').replace(' ', '')

        # Extract numbers
        numbers = re.findall(r'\d+\.?\d*', price_text)
        if numbers:
            try:
                return Decimal(numbers[0])
            except:
                return None
        return None

    def _scrape_lazada_product(self, url):
        """Scrape Lazada Product"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract product data
            title_elem = soup.select_one('h1, .pdp-mod-product-badge-title, [class*="title"]')
            title = title_elem.text.strip() if title_elem else "Unknown Product"

            price_elem = soup.select_one('.pdp-price, [class*="price-box"], [class*="pdp-price"]')
            current_price = self._extract_price(price_elem.text) if price_elem else None

            original_elem = soup.select_one('.pdp-price_type_deleted, [class*="original"]')
            original_price = self._extract_price(original_elem.text) if original_elem else current_price

            image_elem = soup.select_one('.pdp-mod-common-image img, [class*="gallery"] img')
            image_url = image_elem.get('src') if image_elem else None

            # Calculate discount
            discount_percent = None
            if current_price and original_price and original_price > current_price:
                discount_percent = ((original_price - current_price) / original_price * 100)

            # Extract rating
            rating_elem = soup.select_one('[class*="rating-score"], .score-average')
            rating = self._extract_price(rating_elem.text) if rating_elem else None

            # Extract reviews count
            reviews_elem = soup.select_one('[class*="review-count"], .pdp-review-summary')
            reviews_text = reviews_elem.text if reviews_elem else "0"
            reviews_count = int(''.join(filter(str.isdigit, reviews_text))) if reviews_text else 0

            return {
                'platform': 'lazada',
                'title': title,
                'current_price': current_price,
                'original_price': original_price,
                'discount_percent': discount_percent,
                'image_url': image_url,
                'rating': rating,
                'reviews_count': reviews_count,
                'stock_status': 'available',
                'is_available': True,
            }

        except Exception as e:
            print(f"Error scraping Lazada product: {e}")
            return None

    def _scrape_shopee_product(self, url):
        """Scrape Shopee Product"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')

            # Shopee uses a lot of dynamic content, try basic scraping
            title_elem = soup.select_one('h1, [class*="product-title"], [class*="pdp-product-title"]')
            title = title_elem.text.strip() if title_elem else "Unknown Product"

            price_elem = soup.select_one('[class*="product-price"], [class*="pdp-price"]')
            current_price = self._extract_price(price_elem.text) if price_elem else None

            original_elem = soup.select_one('[class*="original-price"]')
            original_price = self._extract_price(original_elem.text) if original_elem else current_price

            image_elem = soup.select_one('[class*="product-image"] img, .product-image img')
            image_url = image_elem.get('src') if image_elem else None

            discount_percent = None
            if current_price and original_price and original_price > current_price:
                discount_percent = ((original_price - current_price) / original_price * 100)

            rating_elem = soup.select_one('[class*="rating-score"]')
            rating = self._extract_price(rating_elem.text) if rating_elem else None

            return {
                'platform': 'shopee',
                'title': title,
                'current_price': current_price,
                'original_price': original_price,
                'discount_percent': discount_percent,
                'image_url': image_url,
                'rating': rating,
                'reviews_count': 0,
                'stock_status': 'available',
                'is_available': True,
            }

        except Exception as e:
            print(f"Error scraping Shopee product: {e}")
            return None

    def _scrape_tiktok_product(self, url):
        """Scrape TikTok Shop Product"""
        try:
            headers_tiktok = {**self.headers, 'Accept-Language': 'th-TH,th;q=0.9'}
            response = requests.get(url, headers=headers_tiktok, timeout=15, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')

            title_elem = soup.select_one('h1, [data-e2e="product-title"]')
            title = title_elem.text.strip() if title_elem else "Unknown Product"

            price_elem = soup.select_one('[data-e2e="product-price"], [class*="price"]')
            current_price = self._extract_price(price_elem.text) if price_elem else None

            return {
                'platform': 'tiktok',
                'title': title,
                'current_price': current_price,
                'original_price': current_price,
                'discount_percent': None,
                'image_url': None,
                'rating': None,
                'reviews_count': 0,
                'stock_status': 'available',
                'is_available': True,
            }

        except Exception as e:
            print(f"Error scraping TikTok product: {e}")
            return None

    def _scrape_taobao_product(self, url):
        """Scrape Taobao Product"""
        try:
            headers_cn = {**self.headers, 'Accept-Language': 'zh-CN,zh;q=0.9'}
            response = requests.get(url, headers=headers_cn, timeout=15, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')

            title_elem = soup.select_one('h1, .tb-main-title, [class*="title"]')
            title = title_elem.text.strip() if title_elem else "Unknown Product"

            price_elem = soup.select_one('.tb-rmb-num, [class*="price"]')
            current_price = self._extract_price(price_elem.text) if price_elem else None

            return {
                'platform': 'taobao',
                'title': title,
                'current_price': current_price,
                'original_price': current_price,
                'discount_percent': None,
                'image_url': None,
                'rating': None,
                'reviews_count': 0,
                'stock_status': 'available',
                'is_available': True,
            }

        except Exception as e:
            print(f"Error scraping Taobao product: {e}")
            return None

    def _scrape_tmall_product(self, url):
        """Scrape Tmall Product"""
        try:
            headers_cn = {**self.headers, 'Accept-Language': 'zh-CN,zh;q=0.9'}
            response = requests.get(url, headers=headers_cn, timeout=15, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')

            title_elem = soup.select_one('h1, .tb-detail-hd, [class*="title"]')
            title = title_elem.text.strip() if title_elem else "Unknown Product"

            price_elem = soup.select_one('.tm-price, [class*="price"]')
            current_price = self._extract_price(price_elem.text) if price_elem else None

            return {
                'platform': 'tmall',
                'title': title,
                'current_price': current_price,
                'original_price': current_price,
                'discount_percent': None,
                'image_url': None,
                'rating': None,
                'reviews_count': 0,
                'stock_status': 'available',
                'is_available': True,
            }

        except Exception as e:
            print(f"Error scraping Tmall product: {e}")
            return None

    def _scrape_pinduoduo_product(self, url):
        """Scrape Pinduoduo Product"""
        try:
            headers_cn = {**self.headers, 'Accept-Language': 'zh-CN,zh;q=0.9'}
            response = requests.get(url, headers=headers_cn, timeout=15, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')

            title_elem = soup.select_one('[class*="goods-name"], [class*="title"]')
            title = title_elem.text.strip() if title_elem else "Unknown Product"

            price_elem = soup.select_one('[class*="price-num"], [class*="group-price"]')
            current_price = self._extract_price(price_elem.text) if price_elem else None

            return {
                'platform': 'pinduoduo',
                'title': title,
                'current_price': current_price,
                'original_price': current_price,
                'discount_percent': None,
                'image_url': None,
                'rating': None,
                'reviews_count': 0,
                'stock_status': 'available',
                'is_available': True,
            }

        except Exception as e:
            print(f"Error scraping Pinduoduo product: {e}")
            return None

    def _scrape_jd_product(self, url):
        """Scrape JD.com (京东) Product"""
        try:
            headers_cn = {**self.headers, 'Accept-Language': 'zh-CN,zh;q=0.9'}
            response = requests.get(url, headers=headers_cn, timeout=15, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')

            # JD.com product title
            title_elem = soup.select_one('.sku-name, .itemInfo-wrap h1, [class*="product-intro"] h1')
            title = title_elem.text.strip() if title_elem else "Unknown Product"

            # JD.com price
            price_elem = soup.select_one('.p-price .price, .summary-price-wrap .price, [class*="price-now"]')
            current_price = self._extract_price(price_elem.text) if price_elem else None

            # Original price (if on sale)
            original_elem = soup.select_one('.summary-price del, [class*="del-price"]')
            original_price = self._extract_price(original_elem.text) if original_elem else current_price

            # Image
            image_elem = soup.select_one('#spec-img, .main-img img, [class*="main-image"] img')
            image_url = image_elem.get('src') or image_elem.get('data-lazy-img') if image_elem else None

            # Calculate discount
            discount_percent = None
            if current_price and original_price and original_price > current_price:
                discount_percent = ((original_price - current_price) / original_price * 100)

            # Rating
            rating_elem = soup.select_one('.comment-percent, [class*="score-average"]')
            rating = self._extract_price(rating_elem.text) if rating_elem else None

            # Reviews count
            reviews_elem = soup.select_one('.comment-count, [class*="comment-count"]')
            reviews_text = reviews_elem.text if reviews_elem else "0"
            reviews_count = int(''.join(filter(str.isdigit, reviews_text))) if reviews_text else 0

            return {
                'platform': 'jd',
                'title': title,
                'current_price': current_price,
                'original_price': original_price,
                'discount_percent': discount_percent,
                'image_url': image_url,
                'rating': rating,
                'reviews_count': reviews_count,
                'stock_status': 'available',
                'is_available': True,
            }

        except Exception as e:
            print(f"Error scraping JD.com product: {e}")
            return None

    def _scrape_1688_product(self, url):
        """Scrape 1688.com Product"""
        try:
            headers_cn = {**self.headers, 'Accept-Language': 'zh-CN,zh;q=0.9'}
            response = requests.get(url, headers=headers_cn, timeout=15, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')

            title_elem = soup.select_one('[class*="title"], h1')
            title = title_elem.text.strip() if title_elem else "Unknown Product"

            price_elem = soup.select_one('[class*="price"], [class*="moq-price"]')
            current_price = self._extract_price(price_elem.text) if price_elem else None

            return {
                'platform': '1688',
                'title': title,
                'current_price': current_price,
                'original_price': current_price,
                'discount_percent': None,
                'image_url': None,
                'rating': None,
                'reviews_count': 0,
                'stock_status': 'available',
                'is_available': True,
            }

        except Exception as e:
            print(f"Error scraping 1688 product: {e}")
            return None

    def _scrape_alibaba_product(self, url):
        """Scrape Alibaba.com Product"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')

            title_elem = soup.select_one('h1, [class*="title"]')
            title = title_elem.text.strip() if title_elem else "Unknown Product"

            price_elem = soup.select_one('[class*="price"], [class*="moq-price"]')
            current_price = self._extract_price(price_elem.text) if price_elem else None

            return {
                'platform': 'alibaba',
                'title': title,
                'current_price': current_price,
                'original_price': current_price,
                'discount_percent': None,
                'image_url': None,
                'rating': None,
                'reviews_count': 0,
                'stock_status': 'available',
                'is_available': True,
            }

        except Exception as e:
            print(f"Error scraping Alibaba product: {e}")
            return None

    def _scrape_aliexpress_product(self, url):
        """Scrape AliExpress Product"""
        try:
            response = requests.get(url, headers=self.headers, timeout=15, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')

            # AliExpress product title
            title_elem = soup.select_one('h1, .product-title, [class*="product-title-text"]')
            title = title_elem.text.strip() if title_elem else "Unknown Product"

            # AliExpress price (often in cents/100)
            price_elem = soup.select_one('.product-price-value, [class*="product-price"]')
            current_price = self._extract_price(price_elem.text) if price_elem else None

            # Original price (if discounted)
            original_elem = soup.select_one('.product-price-original, [class*="original-price"]')
            original_price = self._extract_price(original_elem.text) if original_elem else current_price

            # Image
            image_elem = soup.select_one('.magnifier-image, [class*="product-image"] img')
            image_url = image_elem.get('src') or image_elem.get('data-src') if image_elem else None

            # Calculate discount
            discount_percent = None
            if current_price and original_price and original_price > current_price:
                discount_percent = ((original_price - current_price) / original_price * 100)

            # Rating
            rating_elem = soup.select_one('.overview-rating-average, [class*="rating-num"]')
            rating = self._extract_price(rating_elem.text) if rating_elem else None

            # Reviews count
            reviews_elem = soup.select_one('.product-reviewer-reviews, [class*="review-count"]')
            reviews_text = reviews_elem.text if reviews_elem else "0"
            reviews_count = int(''.join(filter(str.isdigit, reviews_text))) if reviews_text else 0

            # Orders/sold count
            sold_elem = soup.select_one('[class*="order-num"], [class*="sold"]')
            sold_text = sold_elem.text if sold_elem else "0"
            sold_count = int(''.join(filter(str.isdigit, sold_text))) if sold_text else 0

            return {
                'platform': 'aliexpress',
                'title': title,
                'current_price': current_price,
                'original_price': original_price,
                'discount_percent': discount_percent,
                'image_url': image_url,
                'rating': rating,
                'reviews_count': reviews_count,
                'sold_count': sold_count,
                'stock_status': 'available',
                'is_available': True,
            }

        except Exception as e:
            print(f"Error scraping AliExpress product: {e}")
            return None

    def _scrape_amazon_product(self, url):
        """Scrape Amazon Product"""
        try:
            amazon_headers = {
                **self.headers,
                'Accept-Language': 'en-US,en;q=0.9',
            }
            response = requests.get(url, headers=amazon_headers, timeout=15, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')

            title_elem = soup.select_one('#productTitle, h1')
            title = title_elem.text.strip() if title_elem else "Unknown Product"

            price_elem = soup.select_one('.a-price .a-offscreen, #priceblock_ourprice')
            current_price = self._extract_price(price_elem.text) if price_elem else None

            original_elem = soup.select_one('.a-price.a-text-price .a-offscreen')
            original_price = self._extract_price(original_elem.text) if original_elem else current_price

            image_elem = soup.select_one('#landingImage, #imgBlkFront')
            image_url = image_elem.get('src') if image_elem else None

            rating_elem = soup.select_one('.a-icon-star .a-icon-alt')
            rating = self._extract_price(rating_elem.text.split()[0]) if rating_elem else None

            reviews_elem = soup.select_one('#acrCustomerReviewText')
            reviews_text = reviews_elem.text if reviews_elem else "0"
            reviews_count = int(''.join(filter(str.isdigit, reviews_text))) if reviews_text else 0

            discount_percent = None
            if current_price and original_price and original_price > current_price:
                discount_percent = ((original_price - current_price) / original_price * 100)

            return {
                'platform': 'amazon',
                'title': title,
                'current_price': current_price,
                'original_price': original_price,
                'discount_percent': discount_percent,
                'image_url': image_url,
                'rating': rating,
                'reviews_count': reviews_count,
                'stock_status': 'available',
                'is_available': True,
            }

        except Exception as e:
            print(f"Error scraping Amazon product: {e}")
            return None

    def create_or_update_tracked_product(self, product_url, category=None, brand=None, user=None):
        """สร้างหรืออัพเดท TrackedProduct"""
        try:
            # Scrape product data
            product_data = self.scrape_product_by_url(product_url)

            if not product_data:
                print(f"Could not scrape product data from {product_url}")
                return None

            # Check if product already exists
            tracked_product, created = TrackedProduct.objects.get_or_create(
                product_url=product_url,
                defaults={
                    'platform': product_data['platform'],
                    'title': product_data['title'],
                    'current_price': product_data['current_price'],
                    'original_price': product_data['original_price'],
                    'discount_percent': product_data['discount_percent'],
                    'lowest_price': product_data['current_price'],
                    'highest_price': product_data['current_price'],
                    'image_url': product_data.get('image_url'),
                    'rating': product_data.get('rating'),
                    'reviews_count': product_data.get('reviews_count', 0),
                    'sold_count': product_data.get('sold_count', 0),
                    'stock_status': product_data.get('stock_status', 'available'),
                    'is_available': product_data.get('is_available', True),
                    'category': category,
                    'brand': brand,
                    'created_by': user,
                    'last_checked_at': timezone.now(),
                }
            )

            if not created:
                # Update existing product
                tracked_product.title = product_data['title']
                tracked_product.current_price = product_data['current_price']
                tracked_product.original_price = product_data['original_price']
                tracked_product.discount_percent = product_data['discount_percent']
                tracked_product.image_url = product_data.get('image_url')
                tracked_product.rating = product_data.get('rating')
                tracked_product.reviews_count = product_data.get('reviews_count', 0)
                tracked_product.sold_count = product_data.get('sold_count', 0)
                tracked_product.stock_status = product_data.get('stock_status')
                tracked_product.is_available = product_data.get('is_available', True)
                # Update category and brand if they are provided
                if category:
                    tracked_product.category = category
                if brand:
                    tracked_product.brand = brand
                tracked_product.last_checked_at = timezone.now()
                tracked_product.save()

            # Create price history
            if product_data.get('current_price') is not None:
                PriceHistory.objects.create(
                    tracked_product=tracked_product,
                    price=product_data['current_price'],
                    original_price=product_data['original_price'],
                    discount_percent=product_data['discount_percent'],
                    stock_status=product_data.get('stock_status'),
                )

            return tracked_product

        except Exception as e:
            print(f"Error creating/updating tracked product for {product_url}: {e}")
            return None

    def update_all_tracked_products(self):
        """อัพเดทราคาสินค้าทั้งหมดที่ติดตาม"""
        tracked_products = TrackedProduct.objects.filter(is_active=True)
        results = {
            'updated': 0,
            'failed': 0,
            'total': tracked_products.count()
        }

        for product in tracked_products:
            try:
                product_data = self.scrape_product_by_url(product.product_url)

                if product_data and product_data.get('current_price'):
                    product.update_price(product_data['current_price'])
                    product.original_price = product_data.get('original_price')
                    product.discount_percent = product_data.get('discount_percent')
                    product.rating = product_data.get('rating')
                    product.reviews_count = product_data.get('reviews_count', 0)
                    product.stock_status = product_data.get('stock_status')
                    product.is_available = product_data.get('is_available', True)
                    product.save()

                    # Create price history
                    PriceHistory.objects.create(
                        tracked_product=product,
                        price=product_data['current_price'],
                        original_price=product_data.get('original_price'),
                        discount_percent=product_data.get('discount_percent'),
                        stock_status=product_data.get('stock_status'),
                    )

                    results['updated'] += 1
                    print(f"✓ Updated: {product.title}")
                else:
                    results['failed'] += 1
                    print(f"✗ Failed: {product.title}")

            except Exception as e:
                results['failed'] += 1
                print(f"✗ Error updating {product.title}: {e}")

        return results

    # ========== BULK SCRAPING METHODS ==========

    def scrape_category_products(self, platform, category, limit=100):
        """
        Scrape สินค้าตามหมวดหมู่ (Top 100)

        Args:
            platform: แพลตฟอร์ม (lazada, shopee, etc.)
            category: ProductCategory object หรือ category keywords
            limit: จำนวนสินค้าสูงสุด (default: 100)

        Returns:
            list: รายการ product data
        """
        try:
            # ดึง keywords จาก category
            if isinstance(category, ProductCategory):
                keywords = category.keywords or category.name
                category_obj = category
            else:
                keywords = category
                category_obj = None

            # แยก keywords
            keyword_list = [k.strip() for k in keywords.split(',')]
            main_keyword = keyword_list[0] if keyword_list else keywords

            print(f"🔍 Scraping {platform} for category: {main_keyword} (limit: {limit})")

            # เรียก platform-specific bulk scraper
            bulk_scrapers = {
                'lazada': self._scrape_lazada_category,
                'shopee': self._scrape_shopee_category,
                'aliexpress': self._scrape_aliexpress_category,
                'jd': self._scrape_jd_category,
                # Add more platforms as needed
            }

            scraper_method = bulk_scrapers.get(platform)
            if not scraper_method:
                print(f"⚠️ Bulk scraping not yet supported for {platform}")
                return []

            products = scraper_method(main_keyword, limit)

            # บันทึกลง database
            saved_count = 0
            for product_data in products:
                try:
                    tracked_product = self.create_or_update_tracked_product(
                        product_url=product_data.get('product_url', ''),
                        category=category_obj,
                        brand=None
                    )
                    if tracked_product:
                        saved_count += 1
                except Exception as e:
                    print(f"✗ Error saving product: {e}")
                    continue

            print(f"✅ Saved {saved_count}/{len(products)} products to database")
            return products

        except Exception as e:
            print(f"❌ Error scraping category: {e}")
            return []

    def scrape_brand_products(self, platform, brand, limit=100):
        """
        Scrape สินค้าตามแบรนด์ (Top 100)

        Args:
            platform: แพลตฟอร์ม (lazada, shopee, etc.)
            brand: ProductBrand object หรือ brand name
            limit: จำนวนสินค้าสูงสุด (default: 100)

        Returns:
            list: รายการ product data
        """
        try:
            # ดึง brand name
            if isinstance(brand, ProductBrand):
                brand_name = brand.name
                brand_obj = brand
            else:
                brand_name = brand
                brand_obj = None

            print(f"🔍 Scraping {platform} for brand: {brand_name} (limit: {limit})")

            # เรียก platform-specific bulk scraper
            bulk_scrapers = {
                'lazada': self._scrape_lazada_brand,
                'shopee': self._scrape_shopee_brand,
                'aliexpress': self._scrape_aliexpress_brand,
                'jd': self._scrape_jd_brand,
            }

            scraper_method = bulk_scrapers.get(platform)
            if not scraper_method:
                print(f"⚠️ Bulk scraping not yet supported for {platform}")
                return []

            products = scraper_method(brand_name, limit)

            # บันทึกลง database
            saved_count = 0
            for product_data in products:
                try:
                    tracked_product = self.create_or_update_tracked_product(
                        product_url=product_data.get('product_url', ''),
                        category=None,
                        brand=brand_obj
                    )
                    if tracked_product:
                        saved_count += 1
                except Exception as e:
                    print(f"✗ Error saving product: {e}")
                    continue

            print(f"✅ Saved {saved_count}/{len(products)} products to database")
            return products

        except Exception as e:
            print(f"❌ Error scraping brand: {e}")
            return []

    def scrape_best_selling(self, platform, limit=100):
        """
        Scrape สินค้าขายดี/ยอดนิยม (Top 100)

        Args:
            platform: แพลตฟอร์ม (lazada, shopee, etc.)
            limit: จำนวนสินค้าสูงสุด (default: 100)

        Returns:
            list: รายการ product data
        """
        try:
            print(f"🔍 Scraping best-selling products from {platform} (limit: {limit})")

            # เรียก platform-specific best-selling scraper
            bestseller_scrapers = {
                'lazada': self._scrape_lazada_bestsellers,
                'shopee': self._scrape_shopee_bestsellers,
                'aliexpress': self._scrape_aliexpress_bestsellers,
                'jd': self._scrape_jd_bestsellers,
            }

            scraper_method = bestseller_scrapers.get(platform)
            if not scraper_method:
                print(f"⚠️ Best-selling scraping not yet supported for {platform}")
                return []

            products = scraper_method(limit)

            # บันทึกลง database
            saved_count = 0
            for product_data in products:
                try:
                    tracked_product = self.create_or_update_tracked_product(
                        product_url=product_data.get('product_url', ''),
                        category=None,
                        brand=None
                    )
                    if tracked_product:
                        saved_count += 1
                except Exception as e:
                    print(f"✗ Error saving product: {e}")
                    continue

            print(f"✅ Saved {saved_count}/{len(products)} products to database")
            return products

        except Exception as e:
            print(f"❌ Error scraping best-selling: {e}")
            return []

    # ========== PLATFORM-SPECIFIC BULK SCRAPERS ==========

    def _scrape_lazada_category(self, keyword, limit=100):
        """Scrape Lazada category search results

        ⚠️ NOTE: Lazada ใช้ JavaScript โหลดข้อมูล ทำให้ requests ไม่สามารถดึงข้อมูลได้
        ต้องใช้ Selenium หรือ API ของ Lazada

        สำหรับตอนนี้ใช้ DEMO DATA เพื่อแสดงการทำงาน
        """
        products = []

        print(f"⚠️  Lazada requires JavaScript - Using DEMO data for testing")
        print(f"📝 To enable real scraping: Install Selenium or use Lazada API")

        # DEMO DATA สำหรับทดสอบ
        import random
        demo_products = [
            {
                'name_th': 'โทรศัพท์มือถือ Samsung Galaxy S24 Ultra 256GB',
                'name_en': 'Samsung Galaxy S24 Ultra Smartphone 256GB',
                'price_range': (35000, 45000)
            },
            {
                'name_th': 'Apple iPhone 15 Pro Max 256GB',
                'name_en': 'Apple iPhone 15 Pro Max 256GB',
                'price_range': (45000, 55000)
            },
            {
                'name_th': 'กระเป๋าเป้สะพายหลัง แฟชั่น กันน้ำ',
                'name_en': 'Waterproof Fashion Backpack',
                'price_range': (500, 2000)
            },
            {
                'name_th': 'รองเท้าผ้าใบ Nike Air Max สีขาว',
                'name_en': 'Nike Air Max White Sneakers',
                'price_range': (2500, 4500)
            },
            {
                'name_th': 'หูฟังบลูทูธ Sony WH-1000XM5',
                'name_en': 'Sony WH-1000XM5 Bluetooth Headphones',
                'price_range': (8000, 12000)
            },
            {
                'name_th': 'โน้ตบุ๊ค Lenovo IdeaPad Gaming 3',
                'name_en': 'Lenovo IdeaPad Gaming 3 Laptop',
                'price_range': (25000, 35000)
            },
            {
                'name_th': 'นาฬิกาอัจฉริยะ Apple Watch Series 9',
                'name_en': 'Apple Watch Series 9 Smartwatch',
                'price_range': (12000, 18000)
            },
            {
                'name_th': 'กล้อง Canon EOS R6 Mark II Body',
                'name_en': 'Canon EOS R6 Mark II Camera Body',
                'price_range': (75000, 95000)
            },
        ]

        # สุ่มสินค้าตาม keyword
        num_products = min(limit, random.randint(5, 15))

        for i in range(num_products):
            demo = random.choice(demo_products)
            # ใช้ชื่อไทยหรืออังกฤษขึ้นอยู่กับ keyword
            if any(c for c in keyword if ord(c) > 3000):  # มีภาษาไทย
                title = demo['name_th']
            else:
                title = demo['name_en']

            price = Decimal(random.randint(demo['price_range'][0], demo['price_range'][1]))

            products.append({
                'platform': 'lazada',
                'title': f"{title} - DEMO #{i+1}",
                'product_url': f"https://www.lazada.co.th/products/demo-{keyword}-{i+1}-i{random.randint(1000000000, 9999999999)}.html",
                'current_price': price,
                'original_price': price * Decimal('1.2'),  # 20% discount
                'discount_percent': Decimal('20'),
                'image_url': f"https://via.placeholder.com/300x300/4A90E2/FFFFFF?text={title[:20]}",
                'rating': Decimal(str(round(random.uniform(4.0, 5.0), 1))),
                'reviews_count': random.randint(50, 5000),
                'sold_count': random.randint(100, 10000),
                'stock_status': 'available',
                'is_available': True,
            })

        print(f"✅ Generated {len(products)} DEMO products")
        return products

    def _scrape_shopee_category(self, keyword, limit=100):
        """Scrape Shopee category search results

        ⚠️ NOTE: Shopee ใช้ JavaScript โหลดข้อมูล ทำให้ requests ไม่สามารถดึงข้อมูลได้
        ต้องใช้ Selenium หรือ API ของ Shopee

        สำหรับตอนนี้ใช้ DEMO DATA เพื่อแสดงการทำงาน
        """
        products = []

        print(f"⚠️  Shopee requires JavaScript - Using DEMO data for testing")
        print(f"📝 To enable real scraping: Install Selenium or use Shopee API")

        # DEMO DATA สำหรับทดสอบ
        import random
        demo_products = [
            {
                'name_th': 'เสื้อยืดผู้ชาย แฟชั่น คอกลม แขนสั้น',
                'name_en': 'Men Fashion T-Shirt Round Neck Short Sleeve',
                'price_range': (150, 500)
            },
            {
                'name_th': 'กางเกงยีนส์ขายาว ทรงสกินนี่ สีดำ',
                'name_en': 'Skinny Jeans Long Pants Black',
                'price_range': (450, 1200)
            },
            {
                'name_th': 'เครื่องปั่นน้ำผลไม้ พกพา USB',
                'name_en': 'Portable USB Fruit Blender',
                'price_range': (250, 800)
            },
            {
                'name_th': 'ที่ชาร์จไร้สาย 15W Fast Charging',
                'name_en': '15W Wireless Fast Charger',
                'price_range': (300, 900)
            },
            {
                'name_th': 'หมอนหนุน Memory Foam ทรงสูง',
                'name_en': 'Memory Foam High Pillow',
                'price_range': (400, 1500)
            },
            {
                'name_th': 'กระบอกน้ำสแตนเลส เก็บความเย็น 24 ชม.',
                'name_en': 'Stainless Steel Water Bottle 24H Cold',
                'price_range': (350, 1000)
            },
            {
                'name_th': 'รองเท้าแตะ Adidas Adilette Comfort',
                'name_en': 'Adidas Adilette Comfort Slides',
                'price_range': (800, 1500)
            },
            {
                'name_th': 'แป้งดินน้ำมัน กันน้ำ กันเหงื่อ SPF50+',
                'name_en': 'Oil Control Waterproof Powder SPF50+',
                'price_range': (200, 600)
            },
        ]

        # สุ่มสินค้าตาม keyword
        num_products = min(limit, random.randint(8, 20))

        for i in range(num_products):
            demo = random.choice(demo_products)
            # ใช้ชื่อไทยหรืออังกฤษขึ้นอยู่กับ keyword
            if any(c for c in keyword if ord(c) > 3000):  # มีภาษาไทย
                title = demo['name_th']
            else:
                title = demo['name_en']

            price = Decimal(random.randint(demo['price_range'][0], demo['price_range'][1]))

            products.append({
                'platform': 'shopee',
                'title': f"{title} - DEMO #{i+1}",
                'product_url': f"https://shopee.co.th/product/{random.randint(100000000, 999999999)}/{random.randint(1000000000, 9999999999)}",
                'current_price': price,
                'original_price': price * Decimal('1.25'),  # 25% discount
                'discount_percent': Decimal('25'),
                'image_url': f"https://via.placeholder.com/300x300/EE4D2D/FFFFFF?text={title[:20]}",
                'rating': Decimal(str(round(random.uniform(4.2, 5.0), 1))),
                'reviews_count': random.randint(100, 8000),
                'sold_count': random.randint(500, 50000),
                'stock_status': 'available',
                'is_available': True,
            })

        print(f"✅ Generated {len(products)} DEMO products")
        return products

    def _scrape_aliexpress_category(self, keyword, limit=100):
        """Scrape AliExpress category search results

        ⚠️ NOTE: AliExpress ใช้ JavaScript โหลดข้อมูล ทำให้ requests ไม่สามารถดึงข้อมูลได้
        ต้องใช้ Selenium หรือ API ของ AliExpress

        สำหรับตอนนี้ใช้ DEMO DATA เพื่อแสดงการทำงาน
        """
        products = []

        print(f"⚠️  AliExpress requires JavaScript - Using DEMO data for testing")
        print(f"📝 To enable real scraping: Install Selenium or use AliExpress API")

        # DEMO DATA สำหรับทดสอบ
        import random
        demo_products = [
            {
                'name': 'Wireless Bluetooth Earbuds TWS V5.3 Noise Cancelling',
                'price_range': (5, 25)  # USD
            },
            {
                'name': 'LED Desk Lamp USB Rechargeable Touch Control Dimmable',
                'price_range': (8, 30)
            },
            {
                'name': 'Smart Watch Health Monitor Fitness Tracker Waterproof',
                'price_range': (15, 50)
            },
            {
                'name': 'Phone Case Clear Shockproof Protective Cover',
                'price_range': (2, 10)
            },
            {
                'name': 'USB Type-C Cable Fast Charging Data Sync 1m/2m',
                'price_range': (3, 12)
            },
            {
                'name': 'Portable Power Bank 20000mAh Fast Charge Display',
                'price_range': (10, 35)
            },
            {
                'name': 'Kitchen Knife Set Stainless Steel Chef Professional',
                'price_range': (15, 60)
            },
            {
                'name': 'Car Phone Holder Dashboard Mount 360° Rotation',
                'price_range': (4, 15)
            },
            {
                'name': 'Gaming Mouse RGB LED Programmable 7 Buttons DPI',
                'price_range': (8, 30)
            },
            {
                'name': 'Wireless Keyboard Mouse Combo 2.4G Slim Quiet',
                'price_range': (12, 40)
            },
        ]

        # สุ่มสินค้าตาม keyword
        num_products = min(limit, random.randint(10, 25))

        for i in range(num_products):
            demo = random.choice(demo_products)
            title = demo['name']

            price_usd = Decimal(str(random.uniform(demo['price_range'][0], demo['price_range'][1])))
            price_thb = price_usd * Decimal('36')  # Convert USD to THB (approx rate)

            products.append({
                'platform': 'aliexpress',
                'title': f"{title} - DEMO #{i+1}",
                'product_url': f"https://www.aliexpress.com/item/{random.randint(1000000000, 9999999999)}.html",
                'current_price': price_thb.quantize(Decimal('0.01')),
                'original_price': (price_thb * Decimal('1.3')).quantize(Decimal('0.01')),  # 30% discount
                'discount_percent': Decimal('30'),
                'image_url': f"https://via.placeholder.com/300x300/FF6A00/FFFFFF?text={title[:20]}",
                'rating': Decimal(str(round(random.uniform(4.5, 5.0), 1))),
                'reviews_count': random.randint(500, 15000),
                'sold_count': random.randint(1000, 100000),
                'stock_status': 'available',
                'is_available': True,
            })

        print(f"✅ Generated {len(products)} DEMO products")
        return products

    def _scrape_jd_category(self, keyword, limit=100):
        """Scrape JD.com category search results

        ⚠️ NOTE: JD.com (京东) ใช้ JavaScript โหลดข้อมูล ทำให้ requests ไม่สามารถดึงข้อมูลได้
        ต้องใช้ Selenium หรือ API ของ JD.com

        สำหรับตอนนี้ใช้ DEMO DATA เพื่อแสดงการทำงาน
        """
        products = []

        print(f"⚠️  JD.com requires JavaScript - Using DEMO data for testing")
        print(f"📝 To enable real scraping: Install Selenium or use JD.com API")

        # DEMO DATA สำหรับทดสอบ (Chinese e-commerce products)
        import random
        demo_products = [
            {
                'name_cn': '小米13 Pro 智能手机 5G 骁龙8 Gen2',
                'name_en': 'Xiaomi 13 Pro Smartphone 5G Snapdragon 8 Gen2',
                'price_range': (3500, 5500)  # CNY -> THB conversion
            },
            {
                'name_cn': '华为 MatePad Pro 平板电脑 11英寸',
                'name_en': 'Huawei MatePad Pro Tablet 11 inch',
                'price_range': (2800, 4200)
            },
            {
                'name_cn': '联想小新 Pro 16 笔记本电脑 锐龙版',
                'name_en': 'Lenovo Xiaoxin Pro 16 Laptop Ryzen',
                'price_range': (4000, 6500)
            },
            {
                'name_cn': '索尼 WH-1000XM5 无线降噪耳机',
                'name_en': 'Sony WH-1000XM5 Wireless Noise Cancelling Headphones',
                'price_range': (2000, 3000)
            },
            {
                'name_cn': '海尔冰箱 双开门 风冷无霜 520L',
                'name_en': 'Haier Refrigerator Double Door Frost Free 520L',
                'price_range': (3000, 5000)
            },
            {
                'name_cn': '美的空调 1.5匹 变频 冷暖',
                'name_en': 'Midea Air Conditioner 1.5HP Inverter Heat/Cool',
                'price_range': (2500, 4000)
            },
            {
                'name_cn': '戴尔 XPS 15 笔记本电脑 i7处理器',
                'name_en': 'Dell XPS 15 Laptop i7 Processor',
                'price_range': (8000, 12000)
            },
            {
                'name_cn': '九阳破壁机 家用多功能榨汁机',
                'name_en': 'Joyoung Blender Multi-function Juicer',
                'price_range': (400, 1200)
            },
            {
                'name_cn': '科沃斯扫地机器人 智能拖扫一体',
                'name_en': 'Ecovacs Robot Vacuum Smart Sweep and Mop',
                'price_range': (1500, 3500)
            },
            {
                'name_cn': '罗技 MX Master 3S 无线鼠标',
                'name_en': 'Logitech MX Master 3S Wireless Mouse',
                'price_range': (600, 900)
            },
        ]

        # สุ่มสินค้าตาม keyword
        num_products = min(limit, random.randint(12, 30))

        for i in range(num_products):
            demo = random.choice(demo_products)
            # ใช้ชื่อจีนหรืออังกฤษขึ้นอยู่กับ keyword
            if any(c for c in keyword if 0x4e00 <= ord(c) <= 0x9fff):  # มีภาษาจีน
                title = demo['name_cn']
            else:
                title = demo['name_en']

            price_cny = Decimal(random.randint(demo['price_range'][0], demo['price_range'][1]))
            price_thb = price_cny * Decimal('5')  # Convert CNY to THB (approx rate)

            products.append({
                'platform': 'jd',
                'title': f"{title} - DEMO #{i+1}",
                'product_url': f"https://item.jd.com/{random.randint(10000000000, 99999999999)}.html",
                'current_price': price_thb.quantize(Decimal('0.01')),
                'original_price': (price_thb * Decimal('1.15')).quantize(Decimal('0.01')),  # 15% discount
                'discount_percent': Decimal('15'),
                'image_url': f"https://via.placeholder.com/300x300/E3101E/FFFFFF?text={title[:20]}",
                'rating': Decimal(str(round(random.uniform(4.3, 5.0), 1))),
                'reviews_count': random.randint(1000, 50000),
                'sold_count': random.randint(5000, 200000),
                'stock_status': 'available',
                'is_available': True,
            })

        print(f"✅ Generated {len(products)} DEMO products")
        return products

    # Brand scrapers (similar structure)
    def _scrape_lazada_brand(self, brand_name, limit=100):
        """Scrape Lazada brand products"""
        return self._scrape_lazada_category(brand_name, limit)

    def _scrape_shopee_brand(self, brand_name, limit=100):
        """Scrape Shopee brand products"""
        return self._scrape_shopee_category(brand_name, limit)

    def _scrape_aliexpress_brand(self, brand_name, limit=100):
        """Scrape AliExpress brand products"""
        return self._scrape_aliexpress_category(brand_name, limit)

    def _scrape_jd_brand(self, brand_name, limit=100):
        """Scrape JD.com brand products"""
        return self._scrape_jd_category(brand_name, limit)

    # Best-selling scrapers
    def _scrape_lazada_bestsellers(self, limit=100):
        """Scrape Lazada best-selling products"""
        products = []
        try:
            url = "https://www.lazada.co.th/best-sellers/"
            response = requests.get(url, headers=self.headers, timeout=15, verify=False)
            soup = BeautifulSoup(response.content, 'html.parser')

            product_items = soup.select('[data-item-id], .gridItem')[:limit]

            for item in product_items:
                try:
                    title_elem = item.select_one('[class*="title"]')
                    title = title_elem.text.strip() if title_elem else "Unknown"

                    link_elem = item.select_one('a[href]')
                    product_url = link_elem.get('href') if link_elem else None
                    if product_url and not product_url.startswith('http'):
                        product_url = 'https:' + product_url if product_url.startswith('//') else 'https://www.lazada.co.th' + product_url

                    if product_url:
                        products.append({
                            'platform': 'lazada',
                            'title': title,
                            'product_url': product_url,
                        })
                except Exception as e:
                    continue

        except Exception as e:
            print(f"❌ Error scraping Lazada bestsellers: {e}")

        return products

    def _scrape_shopee_bestsellers(self, limit=100):
        """Scrape Shopee best-selling products"""
        return self._scrape_shopee_category("bestseller", limit)

    def _scrape_aliexpress_bestsellers(self, limit=100):
        """Scrape AliExpress best-selling products"""
        return self._scrape_aliexpress_category("hot products", limit)

    def _scrape_jd_bestsellers(self, limit=100):
        """Scrape JD.com best-selling products"""
        return self._scrape_jd_category("热卖", limit)  # 热卖 = hot selling
