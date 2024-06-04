from django.urls import path
from .views import NewsList, NewsDetail, NewsByCategory, create_news, NewsUpdate, NewsDelete


urlpatterns = [
    path('news/', NewsList.as_view(), name='news_list'),  # General news page
    path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),  # News detail page
    path('category/<str:category_name>/', NewsByCategory.as_view(), name='news_by_category'),  # News by category
    path('news/create/', create_news, name='create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_form'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
]