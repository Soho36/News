from django_filters import FilterSet, CharFilter
from .models import News


class NewsFilter(FilterSet):
    category_name = CharFilter(field_name='category__name', lookup_expr='icontains')

    class Meta:
        model = News
        fields = {'name': ['icontains'], 'description': ['icontains']}