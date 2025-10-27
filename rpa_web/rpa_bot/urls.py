from django.urls import path, re_path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Task Management
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    re_path(r'^tasks/(?P<slug>[\w-]+)/$', views.task_detail, name='task_detail'),
    re_path(r'^tasks/(?P<slug>[\w-]+)/edit/$', views.task_update, name='task_update'),
    re_path(r'^tasks/(?P<slug>[\w-]+)/delete/$', views.task_delete, name='task_delete'),

    # Task Execution
    re_path(r'^tasks/(?P<slug>[\w-]+)/run/$', views.task_run, name='task_run'),
    re_path(r'^tasks/(?P<slug>[\w-]+)/stop/$', views.task_stop, name='task_stop'),

    # API Endpoints
    re_path(r'^api/tasks/(?P<slug>[\w-]+)/status/$', views.api_task_status, name='api_task_status'),
    re_path(r'^api/tasks/(?P<slug>[\w-]+)/logs/$', views.api_task_logs, name='api_task_logs'),
    path('api/tasks/create/', views.api_task_create, name='api_task_create'),
    re_path(r'^api/tasks/(?P<slug>[\w-]+)/run/$', views.api_task_run, name='api_task_run'),

    # News Intelligence
    path('news/', views.news_dashboard, name='news_dashboard'),
    path('news/articles/', views.news_articles, name='news_articles'),
    re_path(r'^news/articles/(?P<slug>[\w-]+)/$', views.news_article_detail, name='news_article_detail'),
    re_path(r'^news/articles/(?P<slug>[\w-]+)/analyze/$', views.generate_article_analysis, name='generate_article_analysis'),
    path('news/reports/', views.daily_reports, name='daily_reports'),
    re_path(r'^news/reports/(?P<slug>[\w-]+)/$', views.daily_report_detail, name='daily_report_detail'),
    path('news/scrape/', views.trigger_news_scrape, name='trigger_news_scrape'),
    path('news/generate-report/', views.trigger_generate_report, name='trigger_generate_report'),

    # News API
    path('api/news/stats/', views.api_news_stats, name='api_news_stats'),
    path('api/news/latest-report/', views.api_latest_report, name='api_latest_report'),
    path('api/news/scraping-status/', views.api_scraping_status, name='api_scraping_status'),

    # AI Agent Dashboard
    path('ai-agent/', views.ai_agent_dashboard, name='ai_agent_dashboard'),
    path('api/ai-agent/status/', views.api_ai_agent_status, name='api_ai_agent_status'),
    path('api/ai-agent/discover-stocks/', views.api_ai_agent_discover_stocks, name='api_ai_agent_discover_stocks'),
    path('api/ai-agent/discover-crypto/', views.api_ai_agent_discover_crypto, name='api_ai_agent_discover_crypto'),
    path('api/ai-agent/sentiment/', views.api_ai_agent_sentiment, name='api_ai_agent_sentiment'),

    # E-Commerce Tracking
    path('ecommerce/', views.ecommerce_dashboard, name='ecommerce_dashboard'),
    path('ecommerce/categories/', views.ecommerce_categories, name='ecommerce_categories'),
    path('ecommerce/brands/', views.ecommerce_brands, name='ecommerce_brands'),
    path('ecommerce/product/<int:pk>/', views.tracked_product_detail, name='tracked_product_detail'),

    # E-Commerce API
    path('api/ecommerce/categories/', views.api_ecommerce_categories, name='api_ecommerce_categories'),
    path('api/ecommerce/categories/create/', views.api_ecommerce_category_create, name='api_ecommerce_category_create'),
    path('api/ecommerce/brands/', views.api_ecommerce_brands, name='api_ecommerce_brands'),
    path('api/ecommerce/brands/create/', views.api_ecommerce_brand_create, name='api_ecommerce_brand_create'),
    path('api/ecommerce/tracked-products/', views.api_ecommerce_tracked_products, name='api_ecommerce_tracked_products'),
    path('api/ecommerce/track-url/', views.api_ecommerce_track_url, name='api_ecommerce_track_url'),
    path('api/ecommerce/update-prices/', views.api_ecommerce_update_prices, name='api_ecommerce_update_prices'),
    path('api/ecommerce/update-status/', views.api_ecommerce_update_status, name='api_ecommerce_update_status'),
    path('api/ecommerce/price-history/<int:product_id>/', views.api_ecommerce_price_history, name='api_ecommerce_price_history'),
    path('api/ecommerce/product/<int:product_id>/update/', views.api_ecommerce_product_update, name='api_ecommerce_product_update'),
    path('api/ecommerce/product/<int:product_id>/delete/', views.api_ecommerce_product_delete, name='api_ecommerce_product_delete'),
    path('api/ecommerce/price-alerts/', views.api_ecommerce_price_alerts, name='api_ecommerce_price_alerts'),

    # E-Commerce Bulk Scraping API
    path('api/ecommerce/scrape-category/', views.api_ecommerce_scrape_category, name='api_ecommerce_scrape_category'),
    path('api/ecommerce/scrape-brand/', views.api_ecommerce_scrape_brand, name='api_ecommerce_scrape_brand'),
    path('api/ecommerce/scrape-bestsellers/', views.api_ecommerce_scrape_bestsellers, name='api_ecommerce_scrape_bestsellers'),
    path('api/ecommerce/bulk-scrape-status/', views.api_ecommerce_bulk_scrape_status, name='api_ecommerce_bulk_scrape_status'),

    # Documentation
    path('docs/', views.docs_home, name='docs_home'),
    path('docs/<slug:section>/', views.docs_section, name='docs_section'),
]
