from django.contrib import admin

from .models import Case


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ['case_number', 'title', 'status', 'priority', 'assigned_officer', 'created_at']
    list_filter = ['status', 'priority', 'case_type']
    search_fields = ['case_number', 'title', 'fir_number']
    readonly_fields = ['case_number', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
