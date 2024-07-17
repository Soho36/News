from django.core.management.base import BaseCommand, CommandError
from app.models import Category, News


class Command(BaseCommand):
    help = 'Remove all news from given category'

    def add_arguments(self, parser):
        parser.add_argument(
            'category_name',
            type=str,
            help='Indicates the name of the category from which to delete news'
        )

    def handle(self, *args, **options):
        category_name = options['category_name']
        try:
            category = Category.objects.get(name=category_name)

        except Category.DoesNotExist:
            raise CommandError('Category "%s" does not exist' % category_name)

        news_items = News.objects.filter(category=category)
        if not news_items.exists():
            self.stdout.write(self.style.WARNING('No news items found in category "%s"' % category_name))

        else:
            news_count, _ = News.objects.filter(category=category).delete()
            self.stdout.write(
            self.style.SUCCESS('Successfully deleted %d news items from category "%s"' % (news_count, category_name)))