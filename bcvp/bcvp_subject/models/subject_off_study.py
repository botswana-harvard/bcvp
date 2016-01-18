from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin
from edc_offstudy.models import OffStudyModelMixin
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfModelMixin

from .subject_consent import SubjectConsent
from .subject_visit import SubjectVisit
from edc_meta_data.managers import CrfMetaDataManager


class SubjectOffStudy(OffStudyModelMixin, CrfModelMixin, SyncModelMixin,
                      RequiresConsentMixin, BaseUuidModel):

    """ A model completed by the user on the visit when the subject is taken off-study. """

    consent_model = SubjectConsent

    visit_model_attr = 'subject_visit'

    visit_model = SubjectVisit

    subject_visit = models.OneToOneField(SubjectVisit)

    history = AuditTrail()

    entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = "Subject Off Study"
