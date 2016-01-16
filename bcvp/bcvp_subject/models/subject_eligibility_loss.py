from django.db import models
from django.utils import timezone

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin

from .subject_eligibility import SubjectEligibility


class SubjectEligibilityLossManager(models.Manager):

    def get_by_natural_key(self, eligibility_id):
        subject_eligibility = SubjectEligibility.objects.get_by_natural_key(eligibility_id=eligibility_id)
        return self.get(subject_eligibility=subject_eligibility)


class SubjectEligibilityLoss(SyncModelMixin, BaseUuidModel):
    """ A model triggered and completed by system when a subject is in-eligible. """

    subject_eligibility = models.OneToOneField(SubjectEligibility)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=timezone.now,
        help_text='Date and time of report.')

    reason_ineligible = models.TextField(
        verbose_name='Reason not eligible',
        max_length=500,
        help_text='Gets reasons from Subject Eligibility.reason_ineligible')

    objects = SubjectEligibilityLossManager()

    history = AuditTrail()

    def __unicode__(self):
        return self.get_subject_identifier()

    def natural_key(self):
        return self.subject_eligibility.natural_key()
    natural_key.dependencies = ['bcvp_subject.subjecteligibility']

    def get_subject_identifier(self):
        return self.subject_eligibility.recent_infection.subject_identifier

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = 'Subject Eligibility Loss'
        verbose_name_plural = 'Subject Eligibility Loss'
