from django.db import models
from django.utils import timezone

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_base.model.fields import OtherCharField
from edc_base.model.validators import date_not_future
from edc_death_report.models import Cause
# from edc_death_report.models import DeathReportModelMixin
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_sync.models import SyncModelMixin

from .subject_eligibility import SubjectEligibility


class SubjectDeathReportManager(models.Manager):

    def get_by_natural_key(self, eligibility_id):
        subject_eligibility = SubjectEligibility.objects.get_by_natural_key(eligibility_id=eligibility_id)
        return self.get(subject_eligibility=subject_eligibility)


class SubjectDeathReport(SyncModelMixin, BaseUuidModel):

    """ A model completed by the user on potential participant's death. """

    subject_eligibility = models.OneToOneField(SubjectEligibility)

    last_date_known_alive = models.DateField(
        verbose_name="Date subject refused participation",
        blank=True,
        null=True,
        validators=[date_not_future],
        help_text="Date format is YYYY-MM-DD")

    death_cause = models.ForeignKey(
        to=Cause,
        verbose_name=(
            'What is the primary source of cause of death information? '
            '(if multiple source of information, '
            'list one with the smallest number closest to the top of the list) '),
        null=True)

    cause_other = OtherCharField(
        verbose_name="if other specify...",
        blank=True,
        null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=timezone.now,
        help_text='Date and time of reporting death')

    objects = SubjectDeathReportManager()

    history = AuditTrail()

    def natural_key(self):
        return self.subject_eligibility.natural_key()
    natural_key.dependencies = ['bcvp_subject.subjecteligibility']

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = "Subject Death Report"
