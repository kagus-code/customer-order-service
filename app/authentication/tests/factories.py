import factory
from django.utils import timezone
from factory.django import DjangoModelFactory

from app.authentication.models import User


class UserFactory(DjangoModelFactory):

    class Meta:
        model = User

    mobile = factory.Faker("bothify", text="##########")
    email = factory.Faker("email")
    is_staff = False
    is_active = True
    date_joined = factory.LazyFunction(timezone.now)
