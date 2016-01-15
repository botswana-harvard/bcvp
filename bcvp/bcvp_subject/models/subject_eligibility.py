import uuid

from django.db import models
from django.db.models import get_model

from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc_constants.choices import YES_NO, ALIVE_DEAD, DEAD, ALIVE
from edc_constants.constants import NO, YES
from edc_registration.models import RegisteredSubject
from edc_sync.models import SyncModelMixin

from bcvp.bcvp.constants import MIN_AGE_OF_CONSENT, MAX_AGE_OF_CONSENT

from .recent_infection import RecentInfection
from ..exceptions import NoMatchingRecentInfectionException


class SubjectEligibilityManager(models.Manager):

    def get_by_natural_key(self, eligibility_id):
        return self.get(eligibility_id=eligibility_id)


class SubjectEligibility (SyncModelMixin, BaseUuidModel):
    """ A model completed by the user to test and capture the result of the pre-consent eligibility checks.

    This model has no PII."""

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

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

    survival_status = models.CharField(
        verbose_name="what is the survival status of the participant",
        max_length=5,
        choices=ALIVE_DEAD)

    willing_to_paticipate = models.CharField(
        verbose_name="is the subject willing to participate in the survey?",
        max_length=3,
        choices=YES_NO)

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

    # NullBoolean NULL => Zero State, False => Failed Eligibility, True => Passed Eligibility.
    is_eligible = models.NullBooleanField(
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
        if not self.id:
            self.eligibility_id = str(uuid.uuid4())
        self.is_eligible, error_message = self.check_eligibility()
        self.ineligibility = error_message  # error_message not None if is_eligible is False
        super(SubjectEligibility, self).save(*args, **kwargs)

    def check_eligibility(self):
        """Returns a tuple (True, None) if subject is eligible otherwise (False, error_messsage) where
        error message is the reason for eligibility test failed."""
        error_message = []
        if self.survival_status == DEAD:
            error_message.append('Subject is dead')
        if self.willing_to_paticipate == NO:
            error_message.append('Subject is has refused participation')
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
        return (self.eligibility_id, )

    @property
    def subject_eligibility_loss(self):
        SubjectEligibilityLoss = get_model('bcvp_subject', 'SubjectEligibilityLoss')
        try:
            subject_eligibility_loss = SubjectEligibilityLoss.objects.get(
                subject_eligibility_id=self.id)
        except SubjectEligibilityLoss.DoesNotExist:
            subject_eligibility_loss = None
        return subject_eligibility_loss

    @property
    def recent_infection_record(self):
        """NOTE:This method can be called before registered_suject is created, so DO NOT use any attributes of
        registered_subject."""
        try:
            # Note that using age_in_years is a temporary to be able to get the tests in the right structure.
            # When the fields of RecentInfection and SubjectEligibility are finalized then this will be updated.
            return RecentInfection.objects.get(age_in_years=self.age_in_years)
        except RecentInfection.DoesNotExist:
            raise NoMatchingRecentInfectionException()

    @property
    def subject_death_on_post_save(self):
        """If survival status is dead, then create SubjectDeathReport on post save with a null death_cause and
        last_date_known_alive fields. In UI force user to open and edit this record to enter death_cause and
        last_date_known_alive among others."""
        SubjectEligibilityLoss = get_model('bcvp_subject', 'SubjectEligibilityLoss')
        SubjectDeathReport = get_model('bcvp_subject', 'SubjectDeathReport')
        if self.survival_status == DEAD and not SubjectDeathReport.objects.filter(subject_eligibility=self).exists():
            SubjectDeathReport.objects.create(subject_eligibility=self)
        # Can a person really come back from the dead? maybe, consider witchcraft and religion.
        elif self.survival_status == ALIVE and SubjectDeathReport.objects.filter(subject_eligibility=self).exists():
            SubjectDeathReport.objects.filter(subject_eligibility=self).delete()
            SubjectEligibilityLoss.objects.filter(subject_eligibility_id=self.id).delete()
        # else all is good, do nothing.
        else:
            pass

    @property
    def subject_refusal_on_post_save(self):
        """If willing_to_paticipate is NO, then create SubjectRefusalReport on post save with a null reason and
        refusal_date fields. In UI force user to open and edit this record to enter reason and
        refusal_date among others."""
        SubjectEligibilityLoss = get_model('bcvp_subject', 'SubjectEligibilityLoss')
        SubjectRefusalReport = get_model('bcvp_subject', 'SubjectRefusalReport')
        refusal_report = SubjectRefusalReport.objects.filter(subject_eligibility=self)
        if self.willing_to_paticipate == NO and not refusal_report.exists():
            SubjectRefusalReport.objects.create(subject_eligibility=self)
        # This is necessary for those that initially refuse and later change their mind to participate.
        elif self.willing_to_paticipate == YES and refusal_report.exists():
            SubjectRefusalReport.objects.filter(subject_eligibility=self).delete()
            SubjectEligibilityLoss.objects.filter(subject_eligibility_id=self.id).delete()
        # else all is good, do nothing.
        else:
            pass

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = "Subject Eligibility"
        verbose_name_plural = "Subject Eligibility"
