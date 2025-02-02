from django_filters import (
    CharFilter,
    FilterSet,
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import (
    filters,
    viewsets,
)

from app.customerorders.models import (
    Customer,
    Order,
)
from app.customerorders.serializers import (
    CustomerSerializer,
    OrderCreationSerializer,
    OrderReadSerializer,
)
from app.helpers.custom_pagination import StandardResultsSetPagination


class CustomersFilters(FilterSet):
    """
    Filter set for Customer model.

    Allows filtering customers by name and code.
    - `name`: Performs a case-insensitive search on the `name` field.
    - `code`: Filters customers by the exact `code` field.
    """

    name = CharFilter(field_name="name", lookup_expr="icontains")
    code = CharFilter(field_name="code")


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


class OrdersViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing orders.

    This ViewSet provides CRUD operations for handling orders:

    - `POST`: Creates a new order (`OrderCreationSerializer`).
    - `GET`: Retrieves order details (`OrderReadSerializer`).
    - `PUT`: Updates an order.
    - `PATCH`: Partially updates an order.
    - `DELETE`: Deletes an order.

    The serializer used depends on the request method.
    """

    queryset = Order.objects.all()
    serializer_class = OrderReadSerializer

    def get_serializer_class(self):
        """
        Returns the appropriate serializer based on the request method.

        - `POST`: Uses `OrderCreationSerializer` for order creation.
        - `GET`: Uses `OrderReadSerializer` for retrieving orders.
        - Other methods default to `OrderReadSerializer`.

        Returns:
            Serializer: The appropriate serializer class.
        """
        if self.request.method in ["POST"]:
            return OrderCreationSerializer
        elif self.request.method in ["GET"]:
            return OrderReadSerializer
        return super().get_serializer_class()
