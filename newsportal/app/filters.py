from django_filters import FilterSet, CharFilter, DateFilter
from django.forms.widgets import DateInput
from django.utils.translation import gettext_lazy as _, get_language


class NewsFilter(FilterSet):
    post_name = CharFilter(
        lookup_expr='icontains',
        label=_('Post name contains')
    )
    description = CharFilter(
        lookup_expr='icontains',
        label=_('Description contains')
    )
    category_name = CharFilter(
        lookup_expr='icontains',
        label=_("Category name contains")
    )
    published_date = DateFilter(
        field_name='published_date',
        lookup_expr='gte',
        widget=DateInput(attrs={'type': 'date'}),
        label=_("Published date greater than or equal to")
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        current_language = get_language()

        # Dynamically set the field_name based on the current language
        if current_language == 'ru':
            self.filters['post_name'].field_name = 'name_ru'
            self.filters['description'].field_name = 'description_ru'
            self.filters['category_name'].field_name = 'category__name_ru'
        # The double underscore (__) syntax tells Django to look through the ForeignKey relationship

        else:
            self.filters['post_name'].field_name = 'name_en_us'
            self.filters['description'].field_name = 'description_en_us'
            self.filters['category_name'].field_name = 'category__name_en_us'
        # The double underscore (__) syntax tells Django to look through the ForeignKey relationship


"""
By overriding the __init__ method in the NewsFilter class, 
the field_name for post_name, description and category_name are dynamically set 
based on the current language at the time the filter is instantiated.
When get_language() returns 'ru', the filter's field_name is set to 'name_ru' and 'description_ru', 
so it looks for content in Russian fields.
If the language is anything else (like English), it defaults to 'name_en_us' and 'description_en_us'.
"""