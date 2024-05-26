from django.views.generic import ListView, DetailView
from .models import Product
from django.http import HttpResponse
from datetime import datetime
from pprint import pprint


class ProductsList(ListView):
    model = Product
    ordering = 'name'
    # queryset = Product.objects.filter(price__lt=1000)
    template_name = 'news_list.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        context['next_sale'] = None
        pprint(context)

        return context


class ProductDetail(DetailView):
    model = Product
    template_name = 'news_detail.html'
    context_object_name = 'product'


def home(request):
    return HttpResponse("Welcome to the Home Page")
