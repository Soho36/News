# Register your models here.

from django.contrib import admin
from .models import Category, News, Subscription


admin.site.register(Category)
admin.site.register(News)
admin.site.register(Subscription)
