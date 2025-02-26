from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User
from django.conf import settings
from django.core.mail import send_mail

@receiver(post_save, sender=User)
def send_email_on_create(sender, instance, created, **kwargs):
    if created:
        subject = 'Account created successfully.'
        message = f'Hello {instance.first_name} {instance.last_name} your account created successfully on Skill-Sync\nYour account id: {instance.id}\nEmail: {instance.email}'
        from_email = settings.EMAIL_HOST_USER
        to_email = [instance.email]

        send_mail(subject, message, from_email, to_email)
