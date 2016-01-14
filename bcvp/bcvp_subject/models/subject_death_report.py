from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import date_not_future
from edc_death_report.models import DeathReportModelMixin
from edc_meta_data.managers import CrfMetaDataManager
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfModelMixin
from edc_registration.models import RegisteredSubject


class SubjectDeathReport(SyncModelMixin, DeathReportModelMixin, BaseUuidModel):

    """ A model completed by the user on prticipant's death. """

    registered_subject = models.OneToOneField(RegisteredSubject)

    last_date_known_alive = models.DateField(
        verbose_name="Date subject refused participation",
        validators=[date_not_future],
        help_text="Date format is YYYY-MM-DD")

    objects = models.Manager()

    history = AuditTrail()

    def natural_key(self):
        return self.registered_subject.natural_key()
    natural_key.dependencies = ['edc_registration.registeredsubject']

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = "Subject Death Report"
