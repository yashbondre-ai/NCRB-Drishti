import logging

import django.dispatch
from django.db.models.signals import pre_save
from django.dispatch import receiver

from apps.cases.models import Case

logger = logging.getLogger(__name__)

case_created = django.dispatch.Signal()
case_status_changed = django.dispatch.Signal()
case_assigned = django.dispatch.Signal()


@receiver(case_created)
def handle_case_created(sender, case, created_by, **kwargs):
    logger.info(
        "[AUDIT] Case created: %s (ID: %s) by user %s assigned to %s",
        case.case_number,
        case.id,
        created_by,
        case.assigned_officer,
    )


@receiver(case_status_changed)
def handle_case_status_changed(
    sender, case, previous_status, new_status, changed_by, **kwargs
):
    logger.info(
        "[AUDIT] Case %s status changed: '%s' -> '%s' by %s. Closed date: %s",
        case.case_number,
        previous_status,
        new_status,
        changed_by,
        case.closed_date,
    )


@receiver(pre_save, sender=Case)
def pre_save_case_handler(sender, instance, **kwargs):
    if not instance.case_number:
        from apps.cases.services import CaseService

        instance.case_number = CaseService.generate_case_number()

    if instance.status == Case.Status.CLOSED and not instance.closed_date:
        from django.utils import timezone

        instance.closed_date = timezone.now().date()
    elif instance.status != Case.Status.CLOSED and instance.closed_date:
        instance.closed_date = None
