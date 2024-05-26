from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404
from .models import News, Category


class NewsList(ListView):
    model = News
    ordering = 'name'
    template_name = 'news_list.html'
    context_object_name = 'news_list'


class NewsDetail(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'


class NewsByCategory(ListView):
    template_name = 'news_by_category.html'
    context_object_name = 'news_items'

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['category_name'])
        return News.objects.filter(category=self.category)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

