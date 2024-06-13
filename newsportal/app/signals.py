from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import News, Subscription
from bs4 import BeautifulSoup


@receiver(post_save, sender=News)
def send_new_post_email(sender, instance, created, **kwargs):
    if created:
        subscriptions = Subscription.objects.filter(category=instance.category)
        recipient_list = [subscription.user.email for subscription in subscriptions]
        soup = BeautifulSoup(instance.description, 'html.parser')
        plain_text = soup.get_text()
        post_excerpt = ' '.join(plain_text.split()[:5]) + '...'
        if recipient_list:
            try:
                send_mail(
                    subject=f'New post in {instance.category.name}',
                    message=f'A new post has been added to the {instance.category.name} category!\n{post_excerpt}',
                    from_email='viskey7@yandex.com',
                    recipient_list=recipient_list,
                )
            except Exception as e:
                print(f"Error sending email: {e}")
