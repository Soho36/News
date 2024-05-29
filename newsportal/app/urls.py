from django.urls import path
from .views import NewsList, NewsDetail, NewsByCategory, create_news


urlpatterns = [
    path('news/', NewsList.as_view(), name='news_list'),  # General news page
    path('<int:pk>/', NewsDetail.as_view(), name='news_detail'),  # News detail page
    path('category/<str:category_name>/', NewsByCategory.as_view(), name='news_by_category'),  # News by category
    path('submit_news/', create_news, name='submit_news'),
]