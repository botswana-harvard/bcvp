from edc_call_manager.decorators import register
from edc_call_manager.model_caller import ModelCaller, WEEKLY

from .models import SubjectConsent, SubjectLocator


@register(SubjectConsent)
class SubjectModelCaller(ModelCaller):
    label = 'subject-followup'
    consent_model = SubjectConsent
    locator_model = SubjectLocator
    locator_filter = 'subject_visit__appointment__registered_subject__subject_identifier'
    # unscheduling_model =
    interval = WEEKLY
