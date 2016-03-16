from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin
from edc_meta_data.managers import CrfMetaDataManager
from edc_offstudy.models import OffStudyMixin
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfModelMixin
from edc_export.models import ExportTrackingFieldsMixin

from .subject_consent import SubjectConsent
from .subject_visit import SubjectVisit


class SubjectCrfModel(CrfModelMixin, ExportTrackingFieldsMixin, SyncModelMixin, OffStudyMixin,
                      RequiresConsentMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`SubjectVisit`). """

    consent_model = SubjectConsent

    off_study_model = ('bcvp_subject', 'SubjectOffStudy')

    subject_visit = models.OneToOneField(SubjectVisit)

    history = AuditTrail()

    entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)

    class Meta:
        abstract = True
