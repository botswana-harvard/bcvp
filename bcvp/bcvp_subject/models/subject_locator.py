from django.db import models

from edc_registration.models import RegisteredSubject
from edc_base.audit_trail import AuditTrail
from edc_locator.models import LocatorMixin

from edc_base.model.models import BaseUuidModel
from edc_meta_data.managers import CrfMetaDataManager
from edc_offstudy.models import OffStudyMixin
from edc_sync.models import SyncModelMixin
from edc_visit_tracking.models import CrfModelMixin

from .subject_visit import SubjectVisit


class SubjectLocator(LocatorMixin, CrfModelMixin, SyncModelMixin, OffStudyMixin, BaseUuidModel):

    """ A model completed by the user to capture locator information. """

    off_study_model = ('bcvp_subject', 'SubjectOffStudy')

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    subject_visit = models.OneToOneField(SubjectVisit, null=True)

    history = AuditTrail()

    entry_meta_data_manager = CrfMetaDataManager(SubjectVisit)

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = 'Subject Locator'
        verbose_name_plural = 'Subject Locator'
