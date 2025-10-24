from django.urls import path
from . import views

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Task Management
    path('tasks/', views.task_list, name='task_list'),
    path('tasks/create/', views.task_create, name='task_create'),
    path('tasks/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasks/<int:pk>/edit/', views.task_update, name='task_update'),
    path('tasks/<int:pk>/delete/', views.task_delete, name='task_delete'),

    # Task Execution
    path('tasks/<int:pk>/run/', views.task_run, name='task_run'),
    path('tasks/<int:pk>/stop/', views.task_stop, name='task_stop'),

    # API Endpoints
    path('api/tasks/<int:pk>/status/', views.api_task_status, name='api_task_status'),
    path('api/tasks/<int:pk>/logs/', views.api_task_logs, name='api_task_logs'),
    path('api/tasks/create/', views.api_task_create, name='api_task_create'),
    path('api/tasks/<int:pk>/run/', views.api_task_run, name='api_task_run'),

    # News Intelligence
    path('news/', views.news_dashboard, name='news_dashboard'),
    path('news/articles/', views.news_articles, name='news_articles'),
    path('news/reports/', views.daily_reports, name='daily_reports'),
    path('news/reports/<int:pk>/', views.daily_report_detail, name='daily_report_detail'),
    path('news/scrape/', views.trigger_news_scrape, name='trigger_news_scrape'),
    path('news/generate-report/', views.trigger_generate_report, name='trigger_generate_report'),

    # News API
    path('api/news/stats/', views.api_news_stats, name='api_news_stats'),
    path('api/news/latest-report/', views.api_latest_report, name='api_latest_report'),
]
