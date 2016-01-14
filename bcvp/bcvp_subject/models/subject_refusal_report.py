from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfModelMixin
from edc_base.model.fields import OtherCharField
from edc_base.model.validators import date_not_future, date_not_before_study_start
from edc_constants.choices import WHYNOPARTICIPATE_CHOICE
from edc_registration.models import RegisteredSubject


class SubjectRefusalReport (SyncModelMixin, BaseUuidModel):
    """A model completed by the user that captures reasons for a
    potentially eligible participant refusing participating in BCVP."""
    registered_subject = models.OneToOneField(RegisteredSubject)

    refusal_date = models.DateField(
        verbose_name="Date subject refused participation",
        validators=[date_not_before_study_start, date_not_future],
        help_text="Date format is YYYY-MM-DD")

    reason = models.CharField(
        verbose_name="We respect your decision to decline. It would help us"
                     " improve the study if you could tell us the main reason"
                     " you do not want to participate in this study?",
        max_length=50,
        choices=WHYNOPARTICIPATE_CHOICE,
        help_text="")

    reason_other = OtherCharField()

    history = AuditTrail()

    objects = models.Manager()

    def natural_key(self):
        return self.registered_subject.natural_key()
    natural_key.dependencies = ['edc_registration.registeredsubject']

    def get_registration_datetime(self):
        return self.report_datetime

    def save(self, *args, **kwargs):
        super(SubjectRefusalReport, self).save(*args, **kwargs)

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = "Subject Refusal Report"
