"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views.
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView


urlpatterns = [
    # Root URL
    path(
        "",
        RedirectView.as_view(
            url="/documents/",
            permanent=False,
        ),
    ),

    # Compatibility redirect for Django's default login_required URL
    path(
        "accounts/login/",
        RedirectView.as_view(
            url="/api/auth/login/",
            permanent=False,
        ),
        name="account-login",
    ),

    # Django Admin
    path(
        "admin/",
        admin.site.urls,
    ),

    # Documents API / URLs
    path(
        "documents/",
        include("apps.documents.urls"),
    ),

    # Authentication API
    path(
        "api/auth/",
        include("apps.auth.urls"),
    ),

    # Cases API
    path(
        "api/cases/",
        include("apps.cases.urls"),
    ),
]


# Serve uploaded media files during development
if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )