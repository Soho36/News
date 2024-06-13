from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from .models import News, Subscription


def send_weekly_newsletter():
    today = timezone.now().date()
    last_week = today - timedelta(days=7)

    # Collect new posts from the last week
    new_posts_by_category = {}
    for post in News.objects.filter(published_date__range=(last_week, today)):
        if post.category not in new_posts_by_category:
            new_posts_by_category[post.category] = []
        new_posts_by_category[post.category].append(post)

    # Send an email to subscribers of each category
    for category, posts in new_posts_by_category.items():
        subscriptions = Subscription.objects.filter(category=category)
        recipient_list = [subscription.user.email for subscription in subscriptions]

        if recipient_list:
            post_summaries = "\n".join([f"{post.title}: {post.description[:100]}..." for post in posts])
            send_mail(
                subject=f"Weekly Newsletter: New posts in {category.name}",
                message=f"Here are the new posts in {category.name} from the past week:\n\n{post_summaries}",
                from_email='viskey7@yandex.com',
                recipient_list=recipient_list,
            )
