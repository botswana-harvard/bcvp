from django.db import models

from edc_registration.models import RegisteredSubject
from edc_base.audit_trail import AuditTrail
from edc_locator.models import LocatorMixin

from .subject_crf_model import SubjectCrfModel


class SubjectLocator(LocatorMixin, SubjectCrfModel):

    """ A model completed by the user to capture locator information. """

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    history = AuditTrail()

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = 'Subject Locator'
        verbose_name_plural = 'Subject Locator'
