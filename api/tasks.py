from celery import shared_task
from django.conf import settings
from django.core.mail import send_mail

@shared_task
def send_email_confirmation(order_id, user_email):
    subject = 'Order Confirmation'
    message = f'Your order with {order_id} has successfully received'
    return send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user_email],
    )