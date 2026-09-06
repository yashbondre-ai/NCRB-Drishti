from django.urls import path

from .views import (
    OrganizationListCreateView,
    RegisterView,
    LoginView,
)


urlpatterns = [
    path(
        "organizations/",
        OrganizationListCreateView.as_view(),
        name="organization-list-create",
    ),

    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    
    
    path(
    "login/",
    LoginView.as_view(),
    name="login",
    ),
]