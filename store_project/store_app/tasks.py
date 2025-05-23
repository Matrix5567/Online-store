from django.core.mail import send_mail
from django.conf import settings
from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task()
def send_emails_to_users(mail):
    users_emails = [mail]

    sending_mail = send_mail(
        'Zay Shop',
        'Thankyou for purchasing with us.',
        settings.EMAIL_HOST_USER,
        users_emails,
        fail_silently=False,
    )
    # logger.info("Voila, Email Sent to ")
    return sending_mail
