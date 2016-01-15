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

    # Tying this to a relational of SubjectEligibility instead of RegisteredSubject means that a SubjectEligibilityLoss
    # can only ever be triggered to exist if a SubjectEligibility exists. Implications are that no loss can be created
    # from the call manager. Even if a participant is discovered to be dead from a phone call, the RA still
    # needs to fill the SubjectEligibility for that participant, of which a survival_status=DEAD will lead to the
    # creation of a loss record. The same applies for a participant that refuses.
    subject_eligibility = models.OneToOneField(SubjectEligibility, null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        default=timezone.now,
        help_text='Date and time of report.')

    reason_ineligible = models.TextField(
        verbose_name='Reason not eligible',
        max_length=500,
        help_text='Gets reasons from Subject Eligibility.ineligibility')

    objects = SubjectEligibilityLossManager()

    history = AuditTrail()

    def natural_key(self):
        return self.subject_eligibility.natural_key()
    natural_key.dependencies = ['bcvp_subject.subjecteligibility']

    def ineligibility(self):
        return self.reason_ineligible or []
    reason_ineligible.allow_tags = True

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = 'Subject Eligibility Loss'
        verbose_name_plural = 'Subject Eligibility Loss'
