# Generated by Django 4.2.13 on 2024-08-01 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0013_alter_category_name_alter_category_name_en_us_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(help_text='название категории', max_length=100, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en_us',
            field=models.CharField(help_text='название категории', max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_ru',
            field=models.CharField(help_text='название категории', max_length=100, null=True, unique=True),
        ),
    ]
