from django.urls import path
from .views import NewsList, NewsDetail

urlpatterns = [
   path('', NewsList.as_view()),
   path('<int:pk>', NewsDetail.as_view()),
   path('stock_market/', NewsList.as_view()),
   path('economics/', NewsList.as_view()),
   path('housing/', NewsList.as_view()),
]
