from django.contrib import admin

from app.customerorders.models import (
    Customer,
    Order,
    OrderItem,
)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ("name", "code", "phone", "email", "city", "created_at")
    search_fields = ("name", "code", "phone", "email")
    list_filter = ("city",)
    ordering = ("-created_at",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "customer",
        "total_amount",
        "is_paid",
        "paid_at",
        "is_delivered",
        "delivered_at",
    )
    search_fields = ("code", "customer__name", "customer__code")
    list_filter = ("is_paid", "is_delivered")
    ordering = ("-created_at",)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order", "name", "qty", "price")
    search_fields = ("order__code", "name")
    list_filter = ("order__customer",)
