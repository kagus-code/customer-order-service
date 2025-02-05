import pytest

from app.authentication.models import User
from app.authentication.tests.factories import UserFactory


@pytest.mark.django_db
def test_user_creation():
    user = UserFactory()
    assert user.pk is not None
    assert isinstance(user.mobile, str)
    assert isinstance(user.email, str)
    assert isinstance(user.is_staff, bool)
    assert isinstance(user.is_active, bool)


@pytest.mark.django_db
def test_user_str_representation():
    user = UserFactory(email="example@mail.com")
    assert str(user) == "example@mail.com"


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        email="testuser@mail.com",
        password="securepassword123",
        mobile="1234567890",
    )
    assert user.pk is not None
    assert user.email == "testuser@mail.com"
    assert user.check_password("securepassword123")
    assert user.is_staff is False
    assert user.is_superuser is False


@pytest.mark.django_db
def test_create_user_without_email():
    with pytest.raises(ValueError, match="The Email field must be set"):
        User.objects.create_user(
            email=None, password="securepassword123", mobile="1234567890"
        )


@pytest.mark.django_db
def test_create_superuser():
    superuser = User.objects.create_superuser(
        email="admin@mail.com", password="adminpassword", mobile="0987654321"
    )
    assert superuser.pk is not None
    assert superuser.email == "admin@mail.com"
    assert superuser.check_password("adminpassword")
    assert superuser.is_staff is True
    assert superuser.is_superuser is True


@pytest.mark.django_db
def test_create_superuser_invalid():
    with pytest.raises(ValueError, match="Superuser must have is_staff=True."):
        User.objects.create_superuser(
            email="admin@mail.com",
            password="adminpassword",
            mobile="0987654321",
            is_staff=False,
        )

    with pytest.raises(
        ValueError, match="Superuser must have is_superuser=True."
    ):
        User.objects.create_superuser(
            email="admin@mail.com",
            password="adminpassword",
            mobile="0987654321",
            is_superuser=False,
        )
