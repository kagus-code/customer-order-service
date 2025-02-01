from rest_framework import serializers

from app.customerorders.models import Customer


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        exclude = ("code",)

        extra_kwargs = {
            "name": {"required": True},
            "phone": {"required": True},
            "email": {"required": True},
        }
