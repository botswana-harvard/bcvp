from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_death_report.models import DeathReportModelMixin
from edc_meta_data.managers import CrfMetaDataManager
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfModelMixin

from .subject_visit import SubjectVisit


class SubjectDeathReport(CrfModelMixin, SyncModelMixin, DeathReportModelMixin, BaseUuidModel):

    """ A model completed by the user on the mother's death. """

    subject_visit = models.OneToOneField(SubjectVisit)

    history = AuditTrail()

    entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)

    def natural_key(self):
        return self.subject_visit.natural_key()
    natural_key.dependencies = ['bcvp_subject.subjectvisit']

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = "Subject Death Report"
