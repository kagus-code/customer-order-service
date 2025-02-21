"""
URL configuration for crm project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.contrib import admin
from django.urls import (
    include,
    path,
)
from django.views.generic.base import RedirectView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from decouple import config

schema_view = get_schema_view(
    openapi.Info(
        title="Customer Orders API",
        default_version="v1",
        description="Basic Customer Order service",
        contact=openapi.Contact(email=""),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    url=config("SERVER_URL"),  # Force HTTPS
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("app.customerorders.urls")),
    # swagger URLS
    path(
        "docs/swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path(
        "redoc/",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
    path("oidc/", include("mozilla_django_oidc.urls")),
    # Redirect Django's login URL to OIDC to redirect swagger login and logout functions
    path("accounts/login/", RedirectView.as_view(url="/oidc/authenticate/")),
    path("accounts/logout/", RedirectView.as_view(url="/oidc/logout/")),
]


if not settings.DEBUG:
    urlpatterns += [
        path("", RedirectView.as_view(url="/docs/swagger/")),
    ]
