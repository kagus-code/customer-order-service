from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.timezone import now

from .models import Order


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
