from .models import News, Category
from rest_framework import serializers


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        # fields = '__all__'
        fields = ['id', 'name', 'description', 'category', 'author', 'published_date', ]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', ]
