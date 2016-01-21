from edc_call_manager.decorators import register
from edc_call_manager.model_caller import ModelCaller, WEEKLY

from .models import RecentInfection, SubjectConsent, SubjectLocator


@register(RecentInfection)
class SubjectModelCaller(ModelCaller):
    label = 'MPP Subject'
    locator_model = SubjectLocator
    locator_filter = 'subject_visit__appointment__registered_subject__subject_identifier'
    unscheduling_model = SubjectConsent
    interval = WEEKLY
