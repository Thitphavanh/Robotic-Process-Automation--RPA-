#!/usr/bin/env python
"""
Test script for bulk scraping DEMO data
"""
import os
import sys
import django

# Add project to path
sys.path.append('/Users/hery/Desktop/Robotic-Process-Automation-(RPA) /rpa_web')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')
django.setup()

from rpa_bot.product_scraper import ProductScraperService
from rpa_bot.models import ProductCategory, ProductBrand

def test_category_scraping():
    """Test category scraping with DEMO data"""
    print("\n" + "="*60)
    print("TESTING CATEGORY SCRAPING WITH DEMO DATA")
    print("="*60)

    scraper = ProductScraperService()

    # Test Lazada
    print("\n--- Testing Lazada ---")
    lazada_products = scraper._scrape_lazada_category("smartphone", limit=10)
    print(f"Lazada: Found {len(lazada_products)} products")
    if lazada_products:
        print(f"Sample: {lazada_products[0]['title']} - ฿{lazada_products[0]['current_price']}")

    # Test Shopee
    print("\n--- Testing Shopee ---")
    shopee_products = scraper._scrape_shopee_category("เสื้อผ้า", limit=10)
    print(f"Shopee: Found {len(shopee_products)} products")
    if shopee_products:
        print(f"Sample: {shopee_products[0]['title']} - ฿{shopee_products[0]['current_price']}")

    # Test AliExpress
    print("\n--- Testing AliExpress ---")
    aliexpress_products = scraper._scrape_aliexpress_category("headphones", limit=10)
    print(f"AliExpress: Found {len(aliexpress_products)} products")
    if aliexpress_products:
        print(f"Sample: {aliexpress_products[0]['title']} - ฿{aliexpress_products[0]['current_price']}")

    # Test JD.com
    print("\n--- Testing JD.com ---")
    jd_products = scraper._scrape_jd_category("laptop", limit=10)
    print(f"JD.com: Found {len(jd_products)} products")
    if jd_products:
        print(f"Sample: {jd_products[0]['title']} - ฿{jd_products[0]['current_price']}")

def test_brand_scraping():
    """Test brand scraping with DEMO data"""
    print("\n" + "="*60)
    print("TESTING BRAND SCRAPING WITH DEMO DATA")
    print("="*60)

    scraper = ProductScraperService()

    # Test Lazada brand
    print("\n--- Testing Lazada Brand ---")
    lazada_brand = scraper._scrape_lazada_brand("Samsung", limit=5)
    print(f"Lazada Brand: Found {len(lazada_brand)} products")
    if lazada_brand:
        print(f"Sample: {lazada_brand[0]['title']} - ฿{lazada_brand[0]['current_price']}")

    # Test Shopee brand
    print("\n--- Testing Shopee Brand ---")
    shopee_brand = scraper._scrape_shopee_brand("Nike", limit=5)
    print(f"Shopee Brand: Found {len(shopee_brand)} products")
    if shopee_brand:
        print(f"Sample: {shopee_brand[0]['title']} - ฿{shopee_brand[0]['current_price']}")

def test_full_scraping_workflow():
    """Test full scraping workflow with database"""
    print("\n" + "="*60)
    print("TESTING FULL SCRAPING WORKFLOW (with database)")
    print("="*60)

    scraper = ProductScraperService()

    # Create test category
    category, created = ProductCategory.objects.get_or_create(
        name="Electronics Test",
        defaults={
            'slug': 'electronics-test',
            'keywords': 'smartphone, laptop, tablet',
            'is_active': True
        }
    )
    print(f"\nCategory: {category.name} ({'created' if created else 'exists'})")

    # Test scraping and saving
    print("\n--- Scraping Lazada for category ---")
    products = scraper.scrape_category_products('lazada', category, limit=5)
    print(f"✅ Scraping completed: {len(products)} products")

    # Check database
    from rpa_bot.models import TrackedProduct
    tracked_count = TrackedProduct.objects.filter(category=category).count()
    print(f"✅ Database: {tracked_count} products tracked in this category")

if __name__ == "__main__":
    try:
        test_category_scraping()
        test_brand_scraping()
        test_full_scraping_workflow()

        print("\n" + "="*60)
        print("✅ ALL TESTS COMPLETED SUCCESSFULLY")
        print("="*60)

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
