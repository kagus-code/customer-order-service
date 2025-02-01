import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from app.customerorders.models import (
    Customer,
    Order,
    OrderItem,
)
from app.helpers.generate_codes import (
    generate_unique_code,
    generate_unique_customer_code,
)


class CustomerFactory(DjangoModelFactory):
    class Meta:
        model = Customer

    name = factory.Faker("name")
    code = factory.LazyFunction(generate_unique_customer_code)

    phone = factory.Faker("bothify", text="##########")
    email = factory.Faker("email")

    address = factory.Faker("text", max_nb_chars=50)
    postal_code = factory.Faker("bothify", text="##########")
    city = factory.Faker("city")

    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class OrderFactory(DjangoModelFactory):
    class Meta:
        model = Order

    code = factory.LazyFunction(generate_unique_code)
    customer = factory.SubFactory(CustomerFactory)
    total_amount = factory.Faker(
        "pyfloat", left_digits=5, right_digits=2, positive=True
    )
    is_paid = factory.Faker("boolean")
    paid_at = factory.Maybe(
        "is_paid", factory.LazyFunction(timezone.now), None
    )
    is_delivered = factory.Faker("boolean")
    delivered_at = factory.Maybe(
        "is_delivered", factory.LazyFunction(timezone.now), None
    )

    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)


class OrderItemFactory(DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    name = factory.Faker("word")
    qty = factory.Faker("random_int", min=1, max=100)
    price = factory.Faker(
        "pyfloat", left_digits=5, right_digits=2, positive=True
    )

    created_at = factory.LazyFunction(timezone.now)
    updated_at = factory.LazyFunction(timezone.now)
