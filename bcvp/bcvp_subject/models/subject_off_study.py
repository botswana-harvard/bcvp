from edc_base.audit_trail import AuditTrail
from edc_offstudy.models import OffStudyModelMixin

from .subject_crf_model import SubjectCrfModel
from .subject_consent import SubjectConsent


class SubjectOffStudy(OffStudyModelMixin, SubjectCrfModel):

    """ A model completed by the user on the visit when the subject is taken off-study. """

    consent_model = SubjectConsent

    history = AuditTrail()

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = "Subject Off Study"
