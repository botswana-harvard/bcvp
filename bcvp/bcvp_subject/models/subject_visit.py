from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_consent.models import RequiresConsentMixin
from edc_offstudy.models import OffStudyMixin
from edc_sync.models import SyncModelMixin
from edc_meta_data.models import CrfMetaDataMixin
from edc_visit_tracking.constants import VISIT_REASON_NO_FOLLOW_UP_CHOICES
from edc_visit_tracking.models import VisitModelMixin, PreviousVisitMixin, CaretakerFieldsMixin

from bcvp.bcvp.choices import VISIT_REASON

from .subject_consent import SubjectConsent


class SubjectVisit(OffStudyMixin, SyncModelMixin, PreviousVisitMixin, CrfMetaDataMixin,
                   RequiresConsentMixin, CaretakerFieldsMixin, VisitModelMixin, BaseUuidModel):

    """ Subject visit form."""

    consent_model = SubjectConsent

    off_study_model = ('bcvp_subject', 'SubjectOffStudy')

    history = AuditTrail()

    def __unicode__(self):
        return '{} {} {}'.format(self.appointment.registered_subject.subject_identifier,
                                 self.appointment.registered_subject.first_name,
                                 self.appointment.visit_definition.code)

    def save(self, *args, **kwargs):
        self.subject_identifier = self.appointment.registered_subject.subject_identifier
        super(SubjectVisit, self).save(*args, **kwargs)

    def get_visit_reason_choices(self):
        return VISIT_REASON

    def get_visit_reason_no_follow_up_choices(self):
        """ Returns the visit reasons that do not imply any data
        collection; that is, the subject is not available. """
        dct = {}
        for item in VISIT_REASON_NO_FOLLOW_UP_CHOICES:
            dct.update({item: item})
        return dct

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = 'Subject Visit'
