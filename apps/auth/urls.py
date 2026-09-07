from django.urls import path

from .views import (
    OrganizationListCreateView,
    RegisterView,
    LoginView,
    MyRoleRequestView,
    ActiveRoleListView,
    ActiveOrganizationListView,
    DashboardView,
    RoleRequestApproveView,
    RoleRequestDetailView,
    RoleRequestListView,
    RoleRequestRejectView,
    testing_page,
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
    path("role-requests/", RoleRequestListView.as_view(), name="role-request-list"),
    path("role-requests/<int:pk>/", RoleRequestDetailView.as_view(), name="role-request-detail"),
    path("role-requests/<int:pk>/approve/", RoleRequestApproveView.as_view(), name="role-request-approve"),
    path("role-requests/<int:pk>/reject/", RoleRequestRejectView.as_view(), name="role-request-reject"),
    path("my-role-request/", MyRoleRequestView.as_view(), name="my-role-request"),
    path("roles/", ActiveRoleListView.as_view(), name="active-role-list"),
    path("active-organizations/", ActiveOrganizationListView.as_view(), name="active-organization-list"),
    path("me/", DashboardView.as_view(), name="dashboard"),
    path("testing/register/", testing_page, {"page": "register"}, name="testing-register"),
    path("testing/login/", testing_page, {"page": "login"}, name="testing-login"),
    path("testing/role-requests/", testing_page, {"page": "role-requests"}, name="testing-role-requests"),
    path("testing/dashboard/", testing_page, {"page": "dashboard"}, name="testing-dashboard"),
]