from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import News, Subscription


@receiver(post_save, sender=News)
def send_new_post_email(sender, instance, created, **kwargs):
    if created:
        category_subscribers = Subscription.objects.filter(category=instance.category)
        for subscription in category_subscribers:
            send_mail(
                subject=f'New post in {instance.category.name}',
                message=f'A new post "{instance.title}" has been added to the {instance.category.name} category.',
                from_email='your_email@example.com',
                recipient_list=[subscription.user.email],
            )
