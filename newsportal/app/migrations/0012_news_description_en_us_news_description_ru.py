# Generated by Django 4.2.13 on 2024-07-31 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0011_alter_category_options_alter_news_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='news',
            name='description_en_us',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='news',
            name='description_ru',
            field=models.TextField(null=True),
        ),
    ]
