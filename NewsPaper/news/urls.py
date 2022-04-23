from django.urls import path
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(NewsList.as_view()), name='news_list'),
    path('<int:pk>/', NewsDetails.as_view(), name='post_details'),
    path('category/<slug:slug>/', InCategoryList.as_view(), name='incategory_list'),
    path('category/<slug:slug>/subscribe/', subscribe_for_category, name='subscribe'),
    path('search/', SearchNews.as_view(), name='search_news'),
    path('create/', AddNews.as_view(), name='add_news'),
    path('<int:pk>/edit/', EditNews.as_view(), name='edit_news'),
    path('<int:pk>/delete/', DeleteNews.as_view(), name='delete_news'),
]