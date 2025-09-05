from .base import *  # noqa: F403,F401
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add your production host here
ALLOWED_HOSTS += []  # noqa ignore=F405


STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # noqa ignore=F405
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]


# Enable Whitenoise compression and caching
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"


def get_env_list(var_name, default=None):
    value = os.getenv(var_name, default)
    if value:
        return value.split(",")
    return default or []


ALLOWED_HOSTS += get_env_list("ALLOWED_HOSTS", ["localhost"])  # noqa

CORS_ALLOW_CREDENTIALS = True

CORS_ALLOWED_ORIGINS = get_env_list("CORS_ALLOWED_ORIGINS", [])  # noqa
