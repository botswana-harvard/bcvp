from django.db import models

from edc_appointment.models import AppointmentMixin
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_consent.models.base_consent import BaseConsent
from edc_consent.models.fields import (
    PersonalFieldsMixin, CitizenFieldsMixin, ReviewFieldsMixin, VulnerabilityFieldsMixin)
from edc_consent.models.fields.bw import IdentityFieldsMixin
from edc_identifier.subject.classes import SubjectIdentifier
from edc_offstudy.models import OffStudyMixin
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncModelMixin

from bcvp.bcvp.constants import MIN_AGE_OF_CONSENT, MAX_AGE_OF_CONSENT


class SubjectConsent(BaseConsent, AppointmentMixin, SyncModelMixin, OffStudyMixin, ReviewFieldsMixin,
                     IdentityFieldsMixin, PersonalFieldsMixin,
                     CitizenFieldsMixin, VulnerabilityFieldsMixin, BaseUuidModel):

    """ A model completed by the user on the subject's consent. """

    MIN_AGE_OF_CONSENT = MIN_AGE_OF_CONSENT
    MAX_AGE_OF_CONSENT = MAX_AGE_OF_CONSENT

    off_study_model = ('bcvp_subject', 'SubjectOffStudy')

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    history = AuditTrail()

    def __unicode__(self):
        return '{0} {1} {2} ({3})'.format(self.subject_identifier, self.first_name,
                                          self.last_name, self.initials)

    def save(self, *args, **kwargs):
        if not self.id:
            self.subject_identifier = SubjectIdentifier(
                site_code=self.study_site).get_identifier()
        super(SubjectConsent, self).save(*args, **kwargs)

    def get_registration_datetime(self):
        return self.consent_datetime

    def get_subject_identifier(self):
        return self.subject_identifier

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = 'Subject Consent'
