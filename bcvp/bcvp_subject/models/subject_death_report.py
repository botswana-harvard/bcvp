from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import date_not_future
from edc_death_report.models import DeathReportModelMixin
from edc_sync.models import SyncModelMixin

from .subject_eligibility import SubjectEligibility


class SubjectDeathReportManager(models.Manager):

    def get_by_natural_key(self, eligibility_id):
        subject_eligibility = SubjectEligibility.objects.get_by_natural_key(eligibility_id=eligibility_id)
        return self.get(subject_eligibility=subject_eligibility)


class SubjectDeathReport(SyncModelMixin, DeathReportModelMixin, BaseUuidModel):

    """ A model completed by the user on prticipant's death. """

    subject_eligibility = models.OneToOneField(SubjectEligibility)

    last_date_known_alive = models.DateField(
        verbose_name="Date subject refused participation",
        validators=[date_not_future],
        help_text="Date format is YYYY-MM-DD")

    objects = SubjectDeathReportManager()

    history = AuditTrail()

    def natural_key(self):
        return self.subject_eligibility.natural_key()
    natural_key.dependencies = ['bcvp_subject.subjecteligibility']

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = "Subject Death Report"
