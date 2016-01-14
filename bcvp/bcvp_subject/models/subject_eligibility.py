import uuid

from django.db import models
from django.db.models import get_model

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_constants.choices import YES_NO
from edc_constants.constants import NO
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncModelMixin

from bcvp.bcvp.constants import MIN_AGE_OF_CONSENT, MAX_AGE_OF_CONSENT


class SubjectEligibilityManager(models.Manager):

    def get_by_natural_key(self, eligibility_id, report_datetime):
        return self.get(eligibility_id=eligibility_id, report_datetime=report_datetime)


class SubjectEligibility (SyncModelMixin, BaseUuidModel):
    """ A model completed by the user to test and capture the result of the pre-consent eligibility checks.

    This model has no PII."""

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    eligibility_id = models.CharField(
        verbose_name="Eligibility Identifier",
        max_length=36,
        default=uuid.uuid4,
        editable=False)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        help_text='Date and time of assessing eligibility')

    age_in_years = models.IntegerField(
        verbose_name='What is the age of the participant?')

    has_omang = models.CharField(
        verbose_name="Do you have an OMANG?",
        max_length=3,
        choices=YES_NO)

    ineligibility = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    is_eligible = models.BooleanField(
        default=False,
        editable=False)
    # is updated via signal once subject is consented
    is_consented = models.BooleanField(
        default=False,
        editable=False)
    # updated by signal on saving consent, is determined by participant citizenship
    has_passed_consent = models.BooleanField(
        default=False,
        editable=False)

    objects = SubjectEligibilityManager()

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.is_eligible, error_message = self.check_eligibility()
        self.ineligibility = error_message  # error_message not None if is_eligible is False
        super(SubjectEligibility, self).save(*args, **kwargs)

    def check_eligibility(self):
        """Returns a tuple (True, None) if subject is eligible otherwise (False, error_messsage) where
        error message is the reason for eligibility test failed."""
        error_message = []
        if self.age_in_years < MIN_AGE_OF_CONSENT:
            error_message.append('Subject is under {}'.format(MIN_AGE_OF_CONSENT))
        if self.age_in_years > MAX_AGE_OF_CONSENT:
            error_message.append('Subject is too old (>{})'.format(MAX_AGE_OF_CONSENT))
        if self.has_omang == NO:
            error_message.append('Not a citizen')
        is_eligible = False if error_message else True
        return (is_eligible, ','.join(error_message))

    def __unicode__(self):
        return "{0} ({1})".format(self.eligibility_id, self.age_in_years)

    def natural_key(self):
        return (self.eligibility_id, self.report_datetime, )

    @property
    def subject_eligibility_loss(self):
        SubjectEligibilityLoss = get_model('bcvp_subject', 'SubjectEligibilityLoss')
        try:
            subject_eligibility_loss = SubjectEligibilityLoss.objects.get(
                subject_eligibility_id=self.id)
        except SubjectEligibilityLoss.DoesNotExist:
            subject_eligibility_loss = None
        return subject_eligibility_loss

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = "Subject Eligibility"
        verbose_name_plural = "Subject Eligibility"
