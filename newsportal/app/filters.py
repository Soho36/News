from django_filters import FilterSet, CharFilter, DateFilter
from .models import News
from django.forms.widgets import DateInput


class NewsFilter(FilterSet):
    published_date = DateFilter(
        field_name='published_date',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'})
    )
    category_name = CharFilter(
        field_name='category__name',
        lookup_expr='icontains'
    )

    class Meta:
        model = News
        fields = {
            'name': ['icontains'], 'description': ['icontains']
        }


