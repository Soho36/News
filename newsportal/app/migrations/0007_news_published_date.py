# Generated by Django 4.2.13 on 2024-05-26 13:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_remove_news_price_remove_news_quantity_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='published_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
