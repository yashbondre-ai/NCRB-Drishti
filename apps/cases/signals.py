import logging
import django.dispatch
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from apps.cases.models import Case, CaseStatus

logger = logging.getLogger(__name__)

# Custom domain signals
case_created = django.dispatch.Signal()
case_status_changed = django.dispatch.Signal()
case_assigned = django.dispatch.Signal()


@receiver(case_created)
def handle_case_created(sender, case, created_by, **kwargs):
    """
    Log and handle newly created case events.
    """
    logger.info(
        f"[AUDIT] Case created: {case.case_number} (ID: {case.id}) by user {created_by} "
        f"assigned to {case.assigned_officer}"
    )


@receiver(case_status_changed)
def handle_case_status_changed(sender, case, previous_status, new_status, changed_by, **kwargs):
    """
    Log and handle status transitions, such as closing or reopening cases.
    """
    logger.info(
        f"[AUDIT] Case {case.case_number} status changed: '{previous_status}' -> '{new_status}' "
        f"by {changed_by}. Closed date: {case.closed_date}"
    )


@receiver(pre_save, sender=Case)
def pre_save_case_handler(sender, instance, **kwargs):
    """
    Safety fallback: ensure unique case_number and closed_date management
    if Case is saved directly outside the service layer.
    """
    if not instance.case_number:
        from apps.cases.services import CaseService
        instance.case_number = CaseService.generate_unique_case_number()

    if instance.status == CaseStatus.CLOSED and not instance.closed_date:
        from django.utils import timezone
        instance.closed_date = timezone.now()
    elif instance.status != CaseStatus.CLOSED and instance.closed_date:
        instance.closed_date = None
