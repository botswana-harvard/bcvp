import uuid

from dateutil.relativedelta import relativedelta

from django.core.validators import RegexValidator
from django.db import models
from django.db.models import get_model

from edc_base.audit_trail import AuditTrail
from edc_base.encrypted_fields import EncryptedCharField, IdentityField, FirstnameField, LastnameField
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_constants.choices import YES_NO, ALIVE_DEAD, DEAD, GENDER
from edc_constants.constants import NO, YES
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncModelMixin

from bcvp.bcvp.constants import MIN_AGE_OF_CONSENT, MAX_AGE_OF_CONSENT

from ..exceptions import NoMatchingRecentInfectionException

from .recent_infection import RecentInfection


class SubjectEligibilityManager(models.Manager):

    def get_by_natural_key(self, eligibility_id):
        return self.get(eligibility_id=eligibility_id)


class SubjectEligibility (SyncModelMixin, BaseUuidModel):
    """ A model completed by the user to test and capture the result
    of the pre-consent eligibility checks."""

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    recent_infection = models.OneToOneField(RecentInfection, editable=False)

    eligibility_id = models.CharField(
        verbose_name="Eligibility Identifier",
        max_length=36,
        default=None,
        editable=False)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date and Time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future],
        help_text='Date and time of assessing eligibility')

    first_name = FirstnameField()

    last_name = LastnameField(
        verbose_name="Last name",
        null=True)

    initials = EncryptedCharField(
        validators=[RegexValidator(
            regex=r'^[A-Z]{2,3}$',
            message=('Ensure initials consist of letters '
                     'only in upper case, no spaces.'))])

    gender = models.CharField(
        verbose_name="Gender",
        max_length=1,
        choices=GENDER)

    dob = models.DateField(
        verbose_name="Date of birth",
        help_text="Format is YYYY-MM-DD",
        null=True)

    age_in_years = models.IntegerField(
        verbose_name='Age')

    survival_status = models.CharField(
        verbose_name="Survival status",
        max_length=5,
        choices=ALIVE_DEAD)

    willing_to_participate = models.CharField(
        verbose_name="Is the subject willing to participate in the survey?",
        max_length=3,
        choices=YES_NO,
        null=True,
        blank=True)

    has_omang = models.CharField(
        verbose_name="Is the subject\'s OMANG available to verify identity?",
        max_length=3,
        choices=YES_NO)

    identity = IdentityField()

    is_eligible = models.BooleanField(
        default=False,
        editable=False)

    reason_ineligible = models.TextField(
        verbose_name="Reason not eligible",
        max_length=150,
        null=True,
        editable=False)

    # is updated via signal once subject is consented
    is_consented = models.BooleanField(
        default=False,
        editable=False)

    is_refused = models.BooleanField(
        default=False,
        editable=False)

    # updated by signal on saving consent, is determined by participant citizenship
    has_passed_consent = models.BooleanField(
        default=False,
        editable=False)

    objects = SubjectEligibilityManager()

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.age_in_years = relativedelta(self.report_datetime.date(), self.dob).years
        if not self.id:
            self.eligibility_id = str(uuid.uuid4())
            self.recent_infection = self.get_recent_infection_or_raise()
            self.registered_subject = self.recent_infection.registered_subject
        self.is_eligible, self.reason_ineligible = self.check_eligibility()
        super(SubjectEligibility, self).save(*args, **kwargs)

    def check_eligibility(self):
        """Return a tuple (True, None) if subject is eligible otherwise (False, error_messsage) where
        error message is the reason for eligibility test failed."""
        error_message = []
        if self.survival_status == DEAD:
            error_message.append('deceased')
        if self.willing_to_participate == NO:
            error_message.append('refused participation')
        if self.age_in_years < MIN_AGE_OF_CONSENT:
            error_message.append('under age {}'.format(MIN_AGE_OF_CONSENT))
        if self.age_in_years > MAX_AGE_OF_CONSENT:
            error_message.append('over age {}'.format(MAX_AGE_OF_CONSENT))
        if self.has_omang == NO:
            error_message.append('non-citizen')
        is_eligible = False if error_message else True
        return (is_eligible, ','.join(error_message))

    def __unicode__(self):
        return "{0} ({1})".format(self.eligibility_id, self.age_in_years)

    def natural_key(self):
        return (self.eligibility_id, )

    def get_recent_infection_or_raise(self, exception_cls=None):
        """Return an instance of RecentInfection or raise."""
        exception_cls = exception_cls or NoMatchingRecentInfectionException
        try:
            return RecentInfection.objects.get(
                dob=self.dob, initials=self.initials, identity=self.identity)
        except RecentInfection.DoesNotExist as e:
            raise exception_cls(str(e))

    @property
    def subject_refusal(self):
        SubjectRefusal = get_model('bcvp_subject', 'SubjectRefusal')
        try:
            return SubjectRefusal.objects.get(subject_eligibility=self)
        except SubjectRefusal.DoesNotExist:
            return None

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = "Subject Eligibility"
        verbose_name_plural = "Subject Eligibility"
