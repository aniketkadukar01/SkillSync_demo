from django.conf import settings
from django.core.mail import send_mail
from celery import shared_task

@shared_task()
def send_welcome_email(first_name, last_name, user_id, email):
    """
    Sends a welcome email to a newly created user. methods runs asynchronously.
    celery is utilized for asynchronous task.
    """

    subject = 'Account created successfully.'
    message = f'Hello {first_name} {last_name} your account created successfully on Skill-Sync\nYour account id: {user_id}\nEmail: {email}'
    from_email = settings.EMAIL_HOST_USER
    to_email = [email]

    send_mail(subject, message, from_email, to_email)
