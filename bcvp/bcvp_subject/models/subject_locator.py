from django.db import models
from django.utils import timezone

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_locator.models import LocatorMixin
from edc_offstudy.models import OffStudyMixin
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncModelMixin

from ..managers import LocatorManager

from .subject_off_study import SubjectOffStudy
from .subject_visit import SubjectVisit


class SubjectLocator(LocatorMixin, SyncModelMixin, OffStudyMixin, BaseUuidModel):

    """ A model completed by the user to capture locator information. """

    off_study_model = SubjectOffStudy

    subject_visit = models.OneToOneField(SubjectVisit, null=True)

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        default=timezone.now(),
        help_text='Date and time of assessing eligibility')

    history = AuditTrail()

    objects = LocatorManager()

    def natural_key(self):
        return self.registered_subject.natural_key()
    natural_key.dependencies = ['edc_registration.registeredsubject']

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    def get_report_datetime(self):
        return self.report_datetime

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = 'Subject Locator'
        verbose_name_plural = 'Subject Locator'
