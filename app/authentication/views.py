from django.contrib.auth import get_user_model
from mozilla_django_oidc.auth import OIDCAuthenticationBackend


class CustomOIDCBackend(OIDCAuthenticationBackend):
    def create_user(self, claims):
        """Create a new user based on OIDC claims."""
        email = claims.get("email")
        if not email:
            raise ValueError("Email is required for user creation.")

        User = get_user_model()
        user = User.objects.create_user(email=email)
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.save()
        return user

    def update_user(self, user, claims):
        """Update user information from OIDC claims."""
        user.email = claims.get("email", user.email)
        user.first_name = claims.get("given_name", user.first_name)
        user.last_name = claims.get("family_name", user.last_name)
        user.save()
        return user
