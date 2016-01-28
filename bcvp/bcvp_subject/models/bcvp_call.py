from django.db import models
from django.utils import timezone

from edc_call_manager.models import Call, Log, LogEntry
from edc_constants.constants import NO
from edc_sync.models import SyncModelMixin

from .recent_infection import RecentInfection
from .subject_eligibility import SubjectEligibility


class BcvpCallManager(models.Manager):

    def get_by_natural_key(self, subject_identifier_as_pk):
        return self.get(registered_subject__subject_identifier_as_pk=subject_identifier_as_pk)


class BcvpCall(SyncModelMixin, Call):

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
    def latest_entry(self):
        latest_entry = LogEntry.objects.filter(log__call=self).order_by('-call_datetime')
        if latest_entry.exists():
            return (latest_entry.first().id, latest_entry.first().call_datetime.strftime('%Y-%m-%d %H:%M'))
        else:
            return None

    @property
    def next_call_log(self):
        try:
            Log.objects.get(call=self)
        except Log.DoesNotExist:
            Log.objects.create(call=self)
        latest_entry = LogEntry.objects.filter(log__call=self).order_by('-call_datetime').first()
        if (not latest_entry) or (latest_entry and latest_entry.call_again != NO):
            return (Log.objects.filter(call=self).first().id, timezone.now().strftime('%Y-%m-%d %H:%M'))
        return None

#     objects = BcvpCallManager()

#     def natural_key(self):
#         return (self.subject_identifier, self.label, self.scheduled, )

    def save(self, *args, **kwargs):
        super(BcvpCall, self).save(*args, **kwargs)

    class Meta:
        proxy = True
