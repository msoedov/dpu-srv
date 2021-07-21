"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from drf_yasg import openapi
from django.urls import path
from django.urls import include
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from django.conf.urls import url

from django.contrib import admin

schema_view = get_schema_view(
    openapi.Info(
        title="Secret API",
        default_version="v1",
        description="Api [alpha]",
        terms_of_service="TBD",
        contact=openapi.Contact(email="alexander"),
    ),
    public=True,
    authentication_classes=[],
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = []


urlpatterns = [
    path("hello-admin/", admin.site.urls),
    path("metrics/", include("django_prometheus.urls")),
    path("api/", include("api.urls")),
    path("api/v1/accounts/", include("rest_registration.api.urls")),
    url(
        "api-swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        "api-swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(
        "api-redoc/$",
        schema_view.with_ui("redoc", cache_timeout=0),
        name="schema-redoc",
    ),
]
