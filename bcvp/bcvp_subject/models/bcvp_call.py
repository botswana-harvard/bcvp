from django.utils import timezone
from edc_call_manager.models import Call, Log, LogEntry

from .subject_eligibility import SubjectEligibility
from .recent_infection import RecentInfection


class BcvpCall(Call):

    @property
    def eligibility(self):
        try:
            return SubjectEligibility.objects.get(registered_subject__subject_identifier=self.subject_identifier)
        except SubjectEligibility.DoesNotExist:
            return None

    @property
    def recent_infection(self):
        try:
            return RecentInfection.objects.get(subject_identifier=self.subject_identifier)
        except RecentInfection.DoesNotExist:
            return None

    @property
    def call_entries(self):
        return [(call_entry.id, call_entry.call_datetime.strftime('%Y-%m-%d %H:%M')) for
                call_entry in LogEntry.objects.filter(log__call=self)]

    @property
    def next_call_entry(self):
        try:
            Log.objects.get(call=self)
        except Log.DoesNotExist:
            Log.objects.create(call=self)
        if LogEntry.objects.filter(log__call=self).count() < 3:
            return (Log.objects.filter(call=self).first().id, timezone.now().strftime('%Y-%m-%d %H:%M'))
        else:
            return False

    class Meta:
        proxy = True
