import pytest

from app.customerorders.models import Order
from app.customerorders.tests.factories import (
    CustomerFactory,
    OrderFactory,
    OrderItemFactory,
)


@pytest.mark.django_db
def test_customer_creation():
    customer = CustomerFactory()

    assert customer.id is not None
    assert isinstance(customer.name, str)
    assert isinstance(customer.code, str)
    assert isinstance(customer.phone, str)
    assert isinstance(customer.email, str)
    assert isinstance(customer.address, str)
    assert isinstance(customer.postal_code, str)
    assert isinstance(customer.city, str)


@pytest.mark.django_db
def test_customer_code_uniqueness(db):
    customer1 = CustomerFactory()
    customer2 = CustomerFactory()
    assert customer1.code != customer2.code


@pytest.mark.django_db
def test_customer_str_representation():
    customer = CustomerFactory(name="John Doe", code="ABC123")
    assert str(customer) == "John Doe (ABC123)"


@pytest.mark.django_db
def test_order_creation():
    order = OrderFactory()
    assert order.id is not None
    assert isinstance(order.code, str)
    assert order.customer is not None
    assert isinstance(order.total_amount, (type(None), float))
    assert isinstance(order.is_paid, bool)
    assert isinstance(order.is_delivered, bool)


@pytest.mark.django_db
def test_order_str_representation():
    order = OrderFactory(total_amount=float("100.50"))
    assert str(order) == f"Order {order.customer.code}:({order.total_amount})"


@pytest.mark.django_db
def test_order_item_creation():
    order_item = OrderItemFactory()
    assert order_item.id is not None
    assert isinstance(order_item.order, Order)
    assert isinstance(order_item.name, str)
    assert isinstance(order_item.qty, int)
    assert isinstance(order_item.price, (type(None), float))


@pytest.mark.django_db
def test_order_item_str_representation():
    order_item = OrderItemFactory(name="Widget")
    assert str(order_item) == f"({order_item.order.code}) {order_item.name} "
