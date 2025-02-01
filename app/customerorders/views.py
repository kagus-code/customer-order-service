from django_filters import (
    CharFilter,
    FilterSet,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters,
    viewsets,
)

from app.customerorders.models import Customer
from app.customerorders.serializers import CustomerSerializer
from app.helpers.custom_pagination import StandardResultsSetPagination


class CustomersFilters(FilterSet):
    name = CharFilter(field_name="code", lookup_expr="icontains")
    code = CharFilter(field_name="name")


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.OrderingFilter,
        filters.SearchFilter,
    ]
    filterset_class = CustomersFilters
    pagination_class = StandardResultsSetPagination
    search_fields = ["email", "phone"]
