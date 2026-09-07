from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import RedirectView, TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.auth.urls')),
    path('api/cases/', include('apps.cases.urls')),
    path('documents/api/', include('apps.documents.urls')),
    path('accounts/login/', RedirectView.as_view(url='/login/', permanent=False), name='account-login'),
    path('', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
    path('cases/', TemplateView.as_view(template_name='cases.html'), name='cases'),
    path('documents/', TemplateView.as_view(template_name='documents.html'), name='documents'),
    path('firs/', TemplateView.as_view(template_name='firs.html'), name='firs'),
    path('reports/', TemplateView.as_view(template_name='reports.html'), name='reports'),
    path('ai-assistant/', TemplateView.as_view(template_name='ai_assistant.html'), name='ai_assistant'),
    path('audit-trail/', TemplateView.as_view(template_name='audit_trail.html'), name='audit_trail'),
    path('blockchain/', TemplateView.as_view(template_name='blockchain.html'), name='blockchain'),
    path('users/', TemplateView.as_view(template_name='users.html'), name='users'),
    path('alerts/', TemplateView.as_view(template_name='alerts.html'), name='alerts'),
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('register/', TemplateView.as_view(template_name='registration.html'), name='register'),
    path('registration/', TemplateView.as_view(template_name='registration.html'), name='registration'),
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT,
    )