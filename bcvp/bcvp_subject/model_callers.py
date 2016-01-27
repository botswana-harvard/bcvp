from edc_call_manager.decorators import register
from edc_call_manager.model_caller import ModelCaller, WEEKLY

from .models import RecentInfection, SubjectConsent, SubjectLocator


@register(RecentInfection)
class SubjectModelCaller(ModelCaller):
    label = 'MPP Subject'
    locator_model = SubjectLocator
    locator_filter = 'registered_subject__subject_identifier'
    unscheduling_model = SubjectConsent
    interval = WEEKLY

    def schedule_next_call(self, call, scheduled_date=None):
        """We do not want repeat scheduled calls in vaccine. Just a single call record with several log entries
        attached to it."""
        pass
