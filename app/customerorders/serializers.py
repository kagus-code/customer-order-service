import re
from collections import Counter

from django.db import transaction
from rest_framework import serializers

from app.customerorders.models import (
    Customer,
    Order,
    OrderItem,
)

KENYAN_PHONE_REGEX = r"^(?:\+254|254|07|01)\d{8}$"


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"

        extra_kwargs = {
            "name": {"required": True},
            "phone": {"required": True},
            "email": {"required": True},
            "code": {"read_only": True},
        }

    def validate_phone(self, value):
        """
        Validate and normalize Kenyan phone numbers.

        - Accepts formats: `+2547XXXXXXXX`, `2547XXXXXXXX`, `07XXXXXXXX`, `01XXXXXXXX`.
        - Stores the number in the standard format: `254XXXXXXXXX`.
        """
        value = value.strip().replace(" ", "")  # Remove spaces

        if not re.fullmatch(KENYAN_PHONE_REGEX, value):
            raise serializers.ValidationError(
                "Invalid Kenyan phone number format."
            )

        # Normalize phone number
        value = "254" + value[-9:]

        return value


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = "__all__"

        extra_kwargs = {
            "order": {"read_only": True},
        }


class OrderCreationSerializer(serializers.ModelSerializer):

    order_items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ["customer", "code", "total_amount", "order_items"]

        extra_kwargs = {
            "customer": {"required": True},
            "code": {"read_only": True},
            "total_amount": {"read_only": True},
        }

    def validate_order_items(self, value):
        """
        Strips and validates order item names to prevent duplicates in the same order.
        """
        item_names = []

        for item in value:
            # Strip whitespace from the item name
            item_name = item.get("name", "").strip().lower()
            if not item_name:
                raise serializers.ValidationError(
                    "Order item name cannot be empty."
                )
            item["name"] = item_name  # Update the item name after stripping
            item_names.append(item_name)

        # Check for duplicate names
        duplicates = [
            name for name, count in Counter(item_names).items() if count > 1
        ]
        if duplicates:
            raise serializers.ValidationError(
                f"Duplicate items are not allowed in the same order: {', '.join(duplicates)}"
            )

        return value

    def create(self, validated_data):
        """
        Creates an Order and associated OrderItems.

        - Extracts `order_items` from validated data.
        - Creates an `Order` instance.
        - Creates related `OrderItem` instances.
        - Calculates and saves `total_amount` in the Order.

        Returns:
            Order instance
        """

        order_items_data = validated_data.pop("order_items", [])

        with transaction.atomic():  # Ensures database integrity
            order = Order.objects.create(**validated_data)

            total_amount = sum(
                item.get("price", 0) for item in order_items_data
            )

            # Save order items
            order_items = [
                OrderItem(order=order, **item_data)
                for item_data in order_items_data
            ]
            OrderItem.objects.bulk_create(order_items)

            order.total_amount = total_amount
            order.save(update_fields=["total_amount"])

        return order


class OrderReadSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["customer"] = (
            instance.customer
            and CustomerSerializer(
                instance.customer,
            ).data
        )

        return representation

    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order

        fields = "__all__"

        extra_kwargs = {
            "customer": {"read_only": True},
            "paid_at": {"read_only": True},
            "delivered_at": {"read_only": True},
            "total_amount": {"read_only": True},
        }

    def get_order_items(self, obj):
        order_items = OrderItem.objects.filter(order=obj.id)
        serializer = OrderItemSerializer(order_items, many=True)
        return serializer.data
