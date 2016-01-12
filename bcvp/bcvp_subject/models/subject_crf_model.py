from django.db import models

from edc_meta_data.managers import CrfMetaDataManager
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin
from edc_offstudy.models import OffStudyMixin
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfModelMixin

from .subject_consent import SubjectConsent
from .subject_visit import SubjectVisit


class SubjectCrfModel(CrfModelMixin, SyncModelMixin, OffStudyMixin,
                      RequiresConsentMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`SubjectVisit`). """

    consent_model = SubjectConsent

    off_study_model = ('bcvp_subject', 'SubjectOffStudy')

    subject_visit = models.OneToOneField(SubjectVisit)

    history = AuditTrail()

    entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)

    def natural_key(self):
        return (self.subject_visit.natural_key(), )
    natural_key.dependencies = ['bcvp_subject.subject_visit']

    def __unicode__(self):
        return unicode(self.get_visit())

    class Meta:
        abstract = True
