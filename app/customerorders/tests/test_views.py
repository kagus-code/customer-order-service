import pytest
from rest_framework.test import APIClient

from app.authentication.models import User
from app.customerorders.models import Customer
from app.customerorders.tests.factories import (
    CustomerFactory,
    OrderFactory,
)


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user(db):
    """Create a test user."""
    return User.objects.create_user(
        email="testuser@mail.com", password="testpassword"
    )


@pytest.fixture
def auth_client(api_client, user):
    """Return an API client with authentication."""
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def customer():
    return CustomerFactory()


@pytest.fixture
def order(customer):
    return OrderFactory(customer=customer)


@pytest.mark.django_db
class TestCustomerAPI:
    def test_list_customers(self, auth_client, customer):
        response = auth_client.get("/api/customers/")
        assert response.status_code == 200
        assert len(response.data["results"]) > 0

    def test_filter_customers(self, auth_client, customer):
        response = auth_client.get(f"/api/customers/?name={customer.name}")
        assert response.status_code == 200
        assert customer.name in [
            customer["name"] for customer in response.data["results"]
        ]

    def test_create_customer(self, auth_client):
        payload = {
            "name": "John Doe",
            "phone": "0701234567",
            "email": "user@example.com",
            "address": "string",
            "postal_code": "string",
            "city": "string",
        }
        response = auth_client.post("/api/customers/", payload, format="json")
        assert response.status_code == 201
        assert Customer.objects.filter(name="John Doe").exists()

    def test_invalid_customer_number(self, auth_client):
        payload = {
            "name": "John Doe",
            "phone": "07012345672",
            "email": "user@example.com",
            "address": "string",
            "postal_code": "string",
            "city": "string",
        }
        response = auth_client.post("/api/customers/", payload, format="json")
        assert response.status_code == 400
        assert "Invalid Kenyan phone number format." in str(response.data)


@pytest.mark.django_db
class TestOrderAPI:
    def test_list_orders(self, auth_client, order):
        response = auth_client.get("/api/orders/")
        assert response.status_code == 200
        assert len(response.data["results"]) > 0

    def test_create_order(self, auth_client, customer):
        payload = {
            "customer": customer.id,
            "order_items": [{"name": "string", "qty": 2, "price": 100}],
        }
        response = auth_client.post("/api/orders/", payload, format="json")

        assert response.status_code == 201

    def test_filter_orders(self, auth_client, order):
        response = auth_client.get(
            f"/api/orders/?customer={order.customer.name}"
        )
        assert response.status_code == 200
        assert order.code in [ord["code"] for ord in response.data["results"]]

    def test_empty_name_order(self, auth_client, customer):
        payload = {
            "customer": customer.id,
            "order_items": [{"name": "", "qty": 2, "price": 100}],
        }
        response = auth_client.post("/api/orders/", payload, format="json")

        assert response.status_code == 400
        assert "Order item name cannot be empty." in str(response.data)

    def test_duplicate_item_name(self, auth_client, customer):
        payload = {
            "customer": customer.id,
            "order_items": [
                {"name": "string", "qty": 2, "price": 100},
                {"name": "string", "qty": 2, "price": 200},
            ],
        }
        response = auth_client.post("/api/orders/", payload, format="json")

        assert response.status_code == 400
        assert (
            "Duplicate items are not allowed in the same order: string"
            in str(response.data)
        )

    def test_update_order_is_test(self, auth_client, order):
        payload = {"is_paid": True}

        response = auth_client.patch(
            f"/api/orders/{order.id}/", payload, format="json"
        )

        assert response.status_code == 200

        order.refresh_from_db()
        assert order.is_paid is True
