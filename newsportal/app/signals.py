from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import News
from .tasks import send_new_post_email_task


@receiver(post_save, sender=News)
def send_new_post_email(sender, instance, created, **kwargs):
    if created:
        send_new_post_email_task.delay(instance.id)
