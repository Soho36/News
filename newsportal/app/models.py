from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class News(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='news')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

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


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user} subscribed to {self.category}'
