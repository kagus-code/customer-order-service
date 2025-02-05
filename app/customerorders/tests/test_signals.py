from unittest.mock import patch

import pytest
from django.utils.timezone import now

from app.customerorders.models import (
    Customer,
    Order,
)


@pytest.mark.django_db
class TestOrderSignals:
    @patch("app.tasks.sms.send_sms_notification.delay")
    def test_send_order_confirmation_sms(self, mock_send_sms):
        # Create a customer
        customer = Customer.objects.create(name="John Doe", phone="+123456789")

        # Create an order
        order = Order.objects.create(
            customer=customer, code="ORD123", is_paid=True, is_delivered=False
        )

        # Test if the SMS notification is triggered
        mock_send_sms.assert_called_once_with(
            customer.phone,
            f"Hello {customer.name}, your order {order.code} has been received. ",
        )

    @pytest.mark.parametrize(
        "is_paid, expected_paid_at", [(True, True), (False, None)]
    )
    def test_update_paid_at_timestamp(self, is_paid, expected_paid_at):
        # Create a customer
        customer = Customer.objects.create(name="Jane Doe", phone="+987654321")

        # Create an order
        order = Order.objects.create(
            customer=customer, code="ORD124", is_paid=is_paid, paid_at=None
        )

        # Check the paid_at field
        order.refresh_from_db()
        if expected_paid_at:
            assert order.paid_at is not None
            assert order.paid_at <= now()
        else:
            assert order.paid_at is None

    @pytest.mark.parametrize(
        "is_delivered, expected_delivered_at", [(True, True), (False, None)]
    )
    def test_update_delivered_at_timestamp(
        self, is_delivered, expected_delivered_at
    ):
        # Create a customer
        customer = Customer.objects.create(
            name="Alex Smith", phone="+1122334455"
        )

        # Create an order
        order = Order.objects.create(
            customer=customer,
            code="ORD125",
            is_delivered=is_delivered,
            delivered_at=None,
        )

        # Check the delivered_at field
        order.refresh_from_db()
        if expected_delivered_at:
            assert order.delivered_at is not None
            assert order.delivered_at <= now()
        else:
            assert order.delivered_at is None
