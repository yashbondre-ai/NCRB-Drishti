from django.db import models
from django.conf import settings
from django.utils import timezone


class Case(models.Model):
	"""A case registered and tracked by the secure document system."""

	class CaseType(models.TextChoices):
		CRIMINAL = 'CRIMINAL', 'Criminal'
		CIVIL = 'CIVIL', 'Civil'
		INVESTIGATION = 'INVESTIGATION', 'Investigation'

	class Status(models.TextChoices):
		OPEN = 'OPEN', 'Open'
		UNDER_INVESTIGATION = 'UNDER_INVESTIGATION', 'Under Investigation'
		CHARGESHEETED = 'CHARGESHEETED', 'Chargesheeted'
		IN_TRIAL = 'IN_TRIAL', 'In Trial'
		CLOSED = 'CLOSED', 'Closed'
		ARCHIVED = 'ARCHIVED', 'Archived'

	class Priority(models.TextChoices):
		LOW = 'LOW', 'Low'
		MEDIUM = 'MEDIUM', 'Medium'
		HIGH = 'HIGH', 'High'
		CRITICAL = 'CRITICAL', 'Critical'

	case_number = models.CharField(max_length=40, unique=True, db_index=True, editable=False)
	fir_number = models.CharField(max_length=40, blank=True)
	title = models.CharField(max_length=200)
	description = models.TextField(blank=True)
	case_type = models.CharField(max_length=20, choices=CaseType.choices)
	status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
	priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.MEDIUM)
	organization = models.ForeignKey('ncrb_auth.Organization', on_delete=models.PROTECT, related_name='cases')
	assigned_officer = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True,
		related_name='assigned_cases'
	)
	created_by = models.ForeignKey(
		settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='created_cases'
	)
	opened_date = models.DateField(auto_now_add=True)
	closed_date = models.DateField(null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		db_table = 'cases'
		ordering = ['-created_at']
		indexes = [
			models.Index(fields=['case_number', 'status']),
			models.Index(fields=['assigned_officer', 'status']),
			models.Index(fields=['organization', 'status']),
		]

	def save(self, *args, **kwargs):
		if self.status == self.Status.CLOSED and not self.closed_date:
			self.closed_date = timezone.now().date()
		elif self.status != self.Status.CLOSED:
			self.closed_date = None
		super().save(*args, **kwargs)

	def __str__(self):
		return f'{self.case_number} - {self.title}'
