from django.db.models.signals import post_save
from django.dispatch import receiver

from edc_constants.constants import CONSENTED, SCREENED
from edc_registration.models import RegisteredSubject

from .subject_consent import SubjectConsent
from .subject_eligibility import SubjectEligibility
from .subject_eligibility_loss import SubjectEligibilityLoss
from .subject_refusal_report import SubjectRefusalReport


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


@receiver(post_save, weak=False, dispatch_uid="subject_eligibility_on_post_save")
def subject_eligibility_on_post_save(sender, instance, raw, created, using, **kwargs):
    """Creates/Updates RegisteredSubject and creates or deletes SubjectEligibilityLoss

    If participant is consented, does nothing

    * If registered subject does not exist, it will be created and some attrs
      updated from the SubjectEligibility;
    * If registered subject already exists will update some attrs from the SubjectEligibility;
    * If registered subject and consent already exist, does nothing.

    Note: This is the ONLY place RegisteredSubject is created for mothers in this project."""
    if not raw:
        if isinstance(instance, SubjectEligibility) and not kwargs.get('update_fields'):
            if not instance.is_eligible:
                try:
                    subject_eligibility_loss = SubjectEligibilityLoss.objects.get(
                        subject_eligibility_id=instance.id)
                    subject_eligibility_loss.report_datetime = instance.report_datetime
                    subject_eligibility_loss.reason_ineligible = instance.ineligibility
                    subject_eligibility_loss.user_modified = instance.user_modified
                    subject_eligibility_loss.save()
                except SubjectEligibilityLoss.DoesNotExist:
                    SubjectEligibilityLoss.objects.create(
                        subject_eligibility_id=instance.id,
                        report_datetime=instance.report_datetime,
                        reason_ineligible=instance.ineligibility,
                        user_created=instance.user_created,
                        user_modified=instance.user_modified)
            else:
                SubjectEligibilityLoss.objects.filter(subject_eligibility_id=instance.id).delete()
                try:
                    registered_subject = RegisteredSubject.objects.get(
                        screening_identifier=instance.eligibility_id,
                        subject_type='subject')
                    SubjectConsent.objects.get(registered_subject=registered_subject)
                except RegisteredSubject.DoesNotExist:
                    registered_subject = create_registered_subject(instance)
                    instance.registered_subject = registered_subject
                    instance.save()
                except SubjectConsent.DoesNotExist:
                    registered_subject = update_registered_subject(registered_subject, instance)
                    registered_subject.save()
            instance.subject_refusal_on_post_save


@receiver(post_save, weak=False, dispatch_uid="refusal_report_on_post_save")
def refusal_report_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, SubjectRefusalReport):
            instance.subject_eligibility.refusal_filled = True
            instance.subject_eligibility.save(update_fields=['refusal_filled'])


def create_registered_subject(instance):
    return RegisteredSubject.objects.create(
        created=instance.created,
        registration_status=SCREENED,
        screening_datetime=instance.report_datetime,
        screening_identifier=instance.eligibility_id,
        screening_age_in_years=instance.age_in_years,
        subject_type='subject',
        user_created=instance.user_created)


def update_registered_subject(registered_subject, instance):
    registered_subject.registration_status = SCREENED
    registered_subject.screening_datetime = instance.report_datetime
    registered_subject.screening_identifier = instance.eligibility_id
    registered_subject.screening_age_in_years = instance.age_in_years
    registered_subject.subject_type = 'subject'
    registered_subject.user_modified = instance.user_modified
    return registered_subject
