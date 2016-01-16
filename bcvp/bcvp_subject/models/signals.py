from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from edc_constants.constants import CONSENTED, SCREENED, SUBJECT, NO, YES
from edc_registration.models import RegisteredSubject

from .subject_consent import SubjectConsent
from .subject_eligibility import SubjectEligibility
from .subject_eligibility_loss import SubjectEligibilityLoss
from .subject_refusal import SubjectRefusal
from .recent_infection import RecentInfection
from edc_base.utils.age import age
from bcvp.bcvp_subject.models.subject_locator import SubjectLocator


@receiver(post_save, weak=False, dispatch_uid="subject_consent_on_post_save")
def subject_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, SubjectConsent):
            subject_eligibility = SubjectEligibility.objects.get(
                registered_subject=instance.registered_subject)
            subject_eligibility.is_consented = True
            subject_eligibility.save(update_fields=['is_consented'])
            instance.registered_subject.registration_datetime = instance.consent_datetime
            instance.registered_subject.registration_status = CONSENTED
            instance.registered_subject.save(update_fields=['registration_datetime', 'registration_status'])


@receiver(post_save, weak=False, dispatch_uid="recent_infection_on_post_save")
def recent_infection_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Create/Update RegisteredSubject."""
    if not raw:
        if isinstance(instance, RecentInfection) and not kwargs.get('update_fields'):
            try:
                registered_subject = RegisteredSubject.objects.get(
                    subject_identifier=instance.subject_identifier)
                update_registered_subject(registered_subject, instance)
                update_subject_locator(registered_subject, instance)
            except RegisteredSubject.DoesNotExist:
                registered_subject = create_registered_subject(instance)
                instance.registered_subject = registered_subject
                instance.save(update_fields=['registered_subject'])
                create_subject_locator(registered_subject, instance)


@receiver(post_save, weak=False, dispatch_uid="subject_eligibility_on_post_save")
def subject_eligibility_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Update RegisteredSubject and create or delete SubjectEligibilityLoss."""
    if not raw:
        if isinstance(instance, SubjectEligibility) and not kwargs.get('update_fields'):
            if instance.is_eligible:
                SubjectEligibilityLoss.objects.filter(subject_eligibility_id=instance.id).delete()
                registered_subject = RegisteredSubject.objects.get(
                    subject_identifier=instance.recent_infection.subject_identifier)
                instance.registered_subject = registered_subject
                instance.save(update_fields=['registered_subject'])
                try:
                    SubjectConsent.objects.get(registered_subject=registered_subject)
                except SubjectConsent.DoesNotExist:
                    registered_subject = update_registered_subject(registered_subject, instance)
                    registered_subject.save()
            else:
                try:
                    subject_eligibility_loss = SubjectEligibilityLoss.objects.get(
                        subject_eligibility_id=instance.id)
                    subject_eligibility_loss.report_datetime = instance.report_datetime
                    subject_eligibility_loss.reason_ineligible = instance.reason_ineligible
                    subject_eligibility_loss.user_modified = instance.user_modified
                    subject_eligibility_loss.save()
                except SubjectEligibilityLoss.DoesNotExist:
                    SubjectEligibilityLoss.objects.create(
                        subject_eligibility=instance,
                        report_datetime=instance.report_datetime,
                        reason_ineligible=instance.reason_ineligible,
                        user_created=instance.user_created,
                        user_modified=instance.user_modified)
            create_or_delete_subject_refusal(subject_eligibility=instance)


def create_or_delete_subject_refusal(subject_eligibility):
    """Create subject refusal report if not willing to participate, otherwise delete."""
    if subject_eligibility.willing_to_participate == NO:
        try:
            SubjectRefusal.objects.get(subject_eligibility=subject_eligibility)
        except SubjectRefusal.DoesNotExist:
            SubjectRefusal.objects.create(subject_eligibility=subject_eligibility)
    elif subject_eligibility.willing_to_participate == YES:
        SubjectRefusal.objects.filter(subject_eligibility=subject_eligibility).delete()


@receiver(post_save, weak=False, dispatch_uid="refusal_report_on_post_save")
def refusal_report_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, SubjectRefusal):
            instance.subject_eligibility.is_refused = True
            instance.subject_eligibility.save(update_fields=['is_refused'])


@receiver(post_delete, weak=False, dispatch_uid="refusal_report_on_delete")
def refusal_report_on_delete(sender, instance, using, **kwargs):
    if isinstance(instance, SubjectRefusal):
        instance.subject_eligibility.is_refused = False
        instance.subject_eligibility.save(update_fields=['is_refused'])


def create_subject_locator(registered_subject, recent_infection):
    return SubjectLocator.objects.create(
        user_created=registered_subject.user_created,
        registered_subject=registered_subject,
        subject_cell=recent_infection.subject_cell,
        subject_cell_alt=recent_infection.subject_cell_alt)


def update_subject_locator(registered_subject, recent_infection):
    subject_locator = SubjectLocator.objects.get(registered_subject=registered_subject)
    subject_locator.subject_cell = recent_infection.subject_cell
    subject_locator.subject_cell_alt = recent_infection.subject_cell_alt
    subject_locator.save()


def create_registered_subject(instance):
    return RegisteredSubject.objects.create(
        created=instance.created,
        user_created=instance.user_created,
        registration_status=SCREENED,
        screening_datetime=instance.report_datetime,
        screening_identifier=instance.pk,
        screening_age_in_years=age(instance.dob, instance.report_datetime.date()).years,
        subject_identifier=instance.subject_identifier,
        first_name=instance.first_name,
        dob=instance.dob,
        identity=instance.identity,
        initials=instance.initials,
        subject_type=SUBJECT)


def update_registered_subject(registered_subject, instance):
    registered_subject.first_name = instance.first_name
    registered_subject.identity = instance.identity
    registered_subject.initials = instance.initials
    registered_subject.dob = instance.dob
    registered_subject.registration_status = SCREENED
    registered_subject.screening_datetime = instance.report_datetime
    registered_subject.screening_identifier = instance.pk
    registered_subject.screening_age_in_years = age(instance.dob, instance.report_datetime.date()).years
    registered_subject.subject_type = SUBJECT
    registered_subject.user_modified = instance.user_modified
    registered_subject.save()
    return registered_subject
