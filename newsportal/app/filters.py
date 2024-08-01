from django_filters import FilterSet, CharFilter, DateFilter
from .models import News
from django.forms.widgets import DateInput
from django.utils.translation import gettext_lazy as _


class NewsFilter(FilterSet):
    post_name = CharFilter(
        field_name='name',
        lookup_expr='icontains',
        label=_('Post name contains')
    )
    category_name = CharFilter(
        field_name='category__name',
        lookup_expr='icontains',
        label=_("Category name contains")  # Add translation here
    )
    description = CharFilter(
        field_name='description',
        lookup_expr='icontains',
        label=_('Description contains')
    )

    published_date = DateFilter(
        field_name='published_date',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
        label=_("Published date greater than or equal to")  # Add translation here
    )



