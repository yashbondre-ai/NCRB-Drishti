"""Domain services for case lifecycle operations."""

import uuid

from django.core.exceptions import ValidationError
from django.db.models import Count, Q
from django.utils import timezone

from .models import Case


class CaseService:
    """Encapsulate case numbering, status changes, statistics, and scoping."""

    @staticmethod
    def generate_case_number():
        while True:
            number = f'NCRB/{uuid.uuid4().hex[:8].upper()}'
            if not Case.objects.filter(case_number=number).exists():
                return number

    @classmethod
    def change_status(cls, case, new_status, user):
        valid_statuses = {choice[0] for choice in Case.Status.choices}
        if new_status not in valid_statuses:
            raise ValidationError({'status': 'Invalid case status.'})
        case.status = new_status
        case.closed_date = timezone.now().date() if new_status == Case.Status.CLOSED else None
        case.save(update_fields=['status', 'closed_date', 'updated_at'])
        return case

    @staticmethod
    def get_case_stats(queryset=None):
        queryset = queryset if queryset is not None else Case.objects.all()
        return queryset.aggregate(
            total=Count('id'),
            open=Count('id', filter=Q(status=Case.Status.OPEN)),
            under_investigation=Count('id', filter=Q(status=Case.Status.UNDER_INVESTIGATION)),
            chargesheeted=Count('id', filter=Q(status=Case.Status.CHARGESHEETED)),
            in_trial=Count('id', filter=Q(status=Case.Status.IN_TRIAL)),
            closed=Count('id', filter=Q(status=Case.Status.CLOSED)),
        )

    @staticmethod
    def get_user_cases(user):
        role = str(getattr(user, 'role', '')).upper()
        if role == 'ADMIN' or getattr(user, 'is_superuser', False):
            return Case.objects.all()
        if role == 'OFFICER':
            return Case.objects.filter(Q(assigned_officer=user) | Q(created_by=user)).distinct()
        return Case.objects.filter(organization=getattr(user, 'organization', None))
