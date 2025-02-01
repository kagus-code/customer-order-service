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
    """
    Filter set for Customer model.

    Allows filtering customers by name and code.
    - `name`: Performs a case-insensitive search on the `code` field.
    - `code`: Filters customers by the exact `name` field.
    """

    name = CharFilter(field_name="code", lookup_expr="icontains")
    code = CharFilter(field_name="name")


class CustomerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing customers.

    This endpoint allows users to:
    - Retrieve a list of customers.
    - Search customers by email and phone.
    - Filter by name and code.
    - Apply pagination and ordering.

    Attributes:
        queryset (QuerySet): All Customer objects.
        serializer_class (Serializer): Serializer for Customer model.
        filter_backends (list): Enables filtering, searching, and ordering.
        filterset_class (CustomersFilters): Defines available filters.
        pagination_class (Pagination): Standard pagination settings.
        search_fields (list): Searchable fields (`email` and `phone`).
    """

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
