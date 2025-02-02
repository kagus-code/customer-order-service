from django.db.models.signals import (
    post_save,
    pre_save,
)
from django.dispatch import receiver
from django.utils.timezone import now

from app.tasks.sms import send_sms_notification

from .models import Order


@receiver(post_save, sender=Order)
def send_order_confirmation_sms(sender, instance, created, **kwargs):
    """
    Signal to send an SMS when a new order is created.
    """
    if created:
        customer_phone = instance.customer.phone
        message = f"Hello {instance.customer.name}, your order {instance.code} has been received. "

        send_sms_notification.delay(customer_phone, message)


@receiver(pre_save, sender=Order)
def update_timestamps(sender, instance, **kwargs):
    """
    Updates `paid_at` when `is_paid` is set to True.
    Updates `delivered_at` when `is_delivered` is set to True.
    """
    if instance.is_paid and instance.paid_at is None:
        instance.paid_at = now()

    if instance.is_delivered and instance.delivered_at is None:
        instance.delivered_at = now()
