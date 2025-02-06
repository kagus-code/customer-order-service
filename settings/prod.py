from .base import *  # noqa: F403,F401

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Add your production host here
ALLOWED_HOSTS += []  # noqa ignore=F405

# Whitenoise Settings (Production Only)
MIDDLEWARE.insert(  # noqa ignore=F405
    1, "whitenoise.middleware.WhiteNoiseMiddleware"
)  # noqa ignore=F405


STATIC_URL = "static/"

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # noqa ignore=F405


# Enable Whitenoise compression and caching
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"
