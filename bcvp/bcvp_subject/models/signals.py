from django.db.models.signals import post_save
from django.dispatch import receiver

from edc_constants.constants import CONSENTED

from .subject_consent import SubjectConsent


@receiver(post_save, weak=False, dispatch_uid="subject_consent_on_post_save")
def subject_consent_on_post_save(sender, instance, raw, created, using, **kwargs):
    if not raw:
        if isinstance(instance, SubjectConsent):
            instance.registered_subject.registration_datetime = instance.consent_datetime
            instance.registered_subject.registration_status = CONSENTED
            instance.registered_subject.save(update_fields=['registration_datetime', 'registration_status'])
