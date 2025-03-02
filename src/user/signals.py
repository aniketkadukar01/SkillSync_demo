from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from api.v1.tasks.send_email_on_user_create import send_welcome_email

@receiver(post_save, sender=User)
def send_email_on_create(sender, instance, created, **kwargs):
    if created:
        send_welcome_email.apply_async(args=[instance.first_name, instance.last_name, instance.id, instance.email])
