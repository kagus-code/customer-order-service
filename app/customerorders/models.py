from django.db import models

from app.abstract import TimeStampedModel
from app.helpers.generate_codes import (
    generate_unique_code,
    generate_unique_customer_code,
)


class Customer(TimeStampedModel):
    name = models.CharField(max_length=255)
    code = models.CharField(
        max_length=50,
        unique=True,
        default=generate_unique_customer_code,
        editable=False,
    )
    phone = models.CharField(
        max_length=20,
    )
    email = models.EmailField(max_length=50)
    address = models.CharField(
        max_length=50,
    )
    postal_code = models.CharField(
        max_length=50,
    )
    city = models.CharField(
        max_length=50,
    )

    def __str__(self):
        return f"{self.name} ({self.code})"


class Order(TimeStampedModel):
    code = models.CharField(
        max_length=50, unique=True, default=generate_unique_code, editable=False
    )
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    total_amount = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True
    )
    is_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    is_delivered = models.BooleanField(default=False)
    delivered_at = models.DateTimeField(auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return f"Order {self.customer.code}:(${self.total_amount})"


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    name = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"({self.order.code}) {self.name} "
