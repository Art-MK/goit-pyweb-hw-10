from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('add_author/', views.add_author, name='add_author'),
    path('scrape/', views.scrape_data, name='scrape'),
    path('', views.index, name='index'),
    path('tag/<str:tag>/', views.quotes_by_tag, name='quotes_by_tag'),
    path('search_quotes/', views.search_quotes, name='search_quotes'),
]
