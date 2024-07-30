from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.cache import cache
from django.utils.translation import gettext as _
from django.utils.translation import pgettext_lazy


class News(models.Model):
    name = models.CharField(max_length=150, unique=True)
    description = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)
    category = models.ForeignKey(to='Category', on_delete=models.CASCADE, related_name='news')
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    class Meta:
        verbose_name_plural = _("News")

    def __str__(self):
        return f'{self.name}: {self.description[:20]}'

    def get_absolute_url(self):     # Create new news absolute redirect url
        return f'/news/{self.pk}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)   # Save parent method

        cache.delete(f'news-{self.pk}')     # Delete parent method from cache to reset


class Category(models.Model):

    name = models.CharField(max_length=100, unique=True, help_text=_('category name'))

    class Meta:
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = _("Subscriptions")

    def __str__(self):
        return f'{self.user} subscribed to {self.category}'
