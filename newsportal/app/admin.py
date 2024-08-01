from django.contrib import admin
from .models import Category, News, Subscription
from modeltranslation.admin import TranslationAdmin


class CategoryAdmin(TranslationAdmin):
    model = Category


class NewsAdmin(TranslationAdmin, admin.ModelAdmin):
    # list_display = [field.name for field in News._meta.get_fields()]  # for all available fields
    list_display = ['name', 'category', 'author']
    list_filter = ['name', 'category', 'author']
    search_fields = ['name', 'category__name']


# Register your models here.
admin.site.register(Category, CategoryAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(Subscription)
