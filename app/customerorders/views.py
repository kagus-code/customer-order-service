from rest_framework import (
    filters,
    viewsets,
)

from app.customerorders.models import Customer
from app.customerorders.serializers import CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    http_method_names = [
        "post",
        "get",
    ]
    filter_backends = [filters.SearchFilter]
    search_fields = [
        "name",
        "code",
        "email",
    ]
