from django.urls import path
from .views import (signup, NewsList, NewsDetail, NewsByCategory, create_news, NewsUpdate, NewsDelete, get_author,
                    CustomLoginView, CustomSignupView, subscribe_to_category)
from django.contrib.auth.views import LoginView, LogoutView
from django.views.decorators.cache import cache_page


urlpatterns = [
    # path('news/', NewsList.as_view(), name='news_list'),  # General news page
    # path('news/<int:pk>/', NewsDetail.as_view(), name='news_detail'),  # News detail page

    path('news/', cache_page(60*1)(NewsList.as_view()), name='news_list'),  # General news page caching enabled
    path('news/<int:pk>/', cache_page(60*1)(NewsDetail.as_view()), name='news_detail'),  # News detail page vs caching

    path('category/<str:category_name>/', NewsByCategory.as_view(), name='news_by_category'),  # News by category
    path('news/create/', create_news, name='create'),
    path('news/<int:pk>/edit/', NewsUpdate.as_view(), name='news_form'),
    path('news/<int:pk>/delete/', NewsDelete.as_view(), name='news_delete'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    path('signup/', signup, name='signup'),
    path('get-author/', get_author, name='get_author'),
    path('accounts/login/', CustomLoginView.as_view(), name='account_login'),
    path('accounts/signup/', CustomSignupView.as_view(), name='account_signup'),
    path('category/<int:category_id>/subscribe/', subscribe_to_category, name='subscribe_to_category'),
]
