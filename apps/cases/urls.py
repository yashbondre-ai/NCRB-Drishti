from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.cases.views import CaseViewSet

app_name = 'cases'

router = DefaultRouter()
router.register(r'cases', CaseViewSet, basename='case')

urlpatterns = [
    path('', include(router.urls)),
]
