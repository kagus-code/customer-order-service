"""
Django settings for crm project.

Generated by 'django-admin startproject' using Django 5.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

import os
from pathlib import Path

import dj_database_url
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = config("SECRET_KEY")


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG")


ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "mozilla_django_oidc",
    "django_filters",
    "drf_yasg",
    "app",
    "app.authentication",
    "app.customerorders",
]


AUTHENTICATION_BACKENDS = [
    "app.authentication.views.CustomOIDCBackend",
    "django.contrib.auth.backends.ModelBackend",
]


# Auth0 Configuration
OIDC_RP_CLIENT_ID = config("AUTH0_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = config("AUTH0_CLIENT_SECRET")
OIDC_RP_SIGN_ALGO = "RS256"  # Auth0 uses RS256
OIDC_OP_AUTHORIZATION_ENDPOINT = f"{config("AUTH0_DOMAIN")}/authorize"
OIDC_OP_TOKEN_ENDPOINT = f"{config("AUTH0_DOMAIN")}/oauth/token"
OIDC_OP_USER_ENDPOINT = f"{config("AUTH0_DOMAIN")}/userinfo"
OIDC_OP_JWKS_ENDPOINT = f"{config("AUTH0_DOMAIN")}/.well-known/jwks.json"
OIDC_OP_ISSUER = f"{config("AUTH0_DOMAIN")}/"

# Django login/logout redirection
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = f"{config("AUTH0_DOMAIN")}/v2/logout?client_id={OIDC_RP_CLIENT_ID}&returnTo={config("SERVER_URL")}"

# Configure the JWT validation
OIDC_RP_IDP_SIGN_KEY = None  # Automatically fetch JWKS for RS256
OIDC_RP_SCOPES = "openid profile email"
OIDC_CREATE_USER = True  # Create users in Django upon first login
OIDC_STORE_ACCESS_TOKEN = True
OIDC_STORE_ID_TOKEN = True
OIDC_STORE_REFRESH_TOKEN = True


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "mozilla_django_oidc.contrib.drf.OIDCAuthentication",  # Add OIDC authentication
        "rest_framework.authentication.SessionAuthentication",  # Optional: for browser-based APIs
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",  # Require authentication for all endpoints
    ],
}
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "crm.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "crm.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {"default": dj_database_url.config(default=config("DATABASE_URL"))}

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES["default"].update(db_from_env)

# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "Africa/Nairobi"


USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

MEDIA_URL = "api/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_USER_MODEL = "authentication.User"


SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}
    }
}
