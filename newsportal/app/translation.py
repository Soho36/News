from .models import Category, News, Subscription
from modeltranslation.translator import register, TranslationOptions


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = (
        'name',
    )


@register(News)
class NewsTranslationOptions(TranslationOptions):
    fields = ('name',
              'description',
    )

