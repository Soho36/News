from django.db import models
from time import time
# from django.core.validators import MinValueValidator


class News(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='news')
    published_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "News"

    def __str__(self):
        return f'{self.name}: {self.description[:20]}'


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
