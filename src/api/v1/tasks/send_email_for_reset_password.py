from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task

@shared_task
def send_forgot_password_email(email, link):
    """
    Sends a welcome email on forgot password api, methods runs asynchronously.
    celery is utilized for asynchronous task.
    """
    subject = 'Reset Password.'
    message = f'Hello Sir/Mam\nFor Reset your password click: {link}'
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]
    send_mail(subject, message, from_email, to_email)
