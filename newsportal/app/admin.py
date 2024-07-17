from django.contrib import admin
from .models import Category, News, Subscription


class NewsAdmin(admin.ModelAdmin):
    # list_display = [field.name for field in News._meta.get_fields()]  # for all available fields
    list_display = ['name', 'category', 'author']
    list_filter = ['name', 'category', 'author']
    search_fields = ['name', 'category__name']

# class CategoryAdmin(admin.ModelAdmin):


# Register your models here.
admin.site.register(Category)
admin.site.register(News, NewsAdmin)
admin.site.register(Subscription)
