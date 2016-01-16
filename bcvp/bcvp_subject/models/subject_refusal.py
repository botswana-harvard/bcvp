from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin
from edc_base.model.fields import OtherCharField
from edc_base.model.validators import date_not_future, date_not_before_study_start
from edc_constants.choices import WHYNOPARTICIPATE_CHOICE

from .subject_eligibility import SubjectEligibility


class SubjectRefusalManager(models.Manager):

    def get_by_natural_key(self, eligibility_id):
        subject_eligibility = SubjectEligibility.objects.get_by_natural_key(eligibility_id=eligibility_id)
        return self.get(subject_eligibility=subject_eligibility)


class SubjectRefusal(SyncModelMixin, BaseUuidModel):
    """A model completed by the user that captures reasons for a
    potentially eligible participant refusing to participate."""

    subject_eligibility = models.OneToOneField(SubjectEligibility)

    refusal_date = models.DateField(
        verbose_name="Date subject refused participation",
        validators=[date_not_before_study_start, date_not_future],
        blank=True,
        null=True,
        help_text="Date format is YYYY-MM-DD")

    reason = models.CharField(
        verbose_name="We respect your decision to decline. It would help us"
                     " improve the study if you could tell us the main reason"
                     " you do not want to participate in this study?",
        max_length=50,
        choices=WHYNOPARTICIPATE_CHOICE,
        blank=True,
        null=True,
        help_text="")

    reason_other = OtherCharField()

    objects = SubjectRefusalManager()

    history = AuditTrail()

    def natural_key(self):
        return self.subject_eligibility.natural_key()
    natural_key.dependencies = ['bcvp_subject.subjecteligibility']

    def get_registration_datetime(self):
        return self.report_datetime

    def save(self, *args, **kwargs):
        super(SubjectRefusal, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = "Subject Refusal Report"
