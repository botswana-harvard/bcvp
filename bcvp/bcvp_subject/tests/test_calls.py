from edc_constants.constants import YES, ALIVE
from edc_call_manager.models import Log, LogEntry

from bcvp.bcvp_subject.models import (RecentInfection, BcvpCall)

from .base_test_case import BaseTestCase
from .factories import SubjectEligibilityFactory


class TestCalls(BaseTestCase):

    def setUp(self):
        super(TestCalls, self).setUp()
        self.recent_infection = RecentInfection.objects.first()
        self.data = {
            'dob': self.recent_infection.dob,
            'has_omang': YES,
            'identity': self.recent_infection.identity,
            'initials': self.recent_infection.initials,
            'survival_status': ALIVE,
            'willing_to_participate': YES}

    def test_call_proxy_returns_no_eligibility(self):
        calls = BcvpCall.objects.filter(subject_identifier=self.recent_infection.subject_identifier)
        self.assertEqual(calls.count(), 1)
        call = calls[0]
        self.assertIsNone(call.eligibility)

    def test_call_proxy_returns_eligibility(self):
        calls = BcvpCall.objects.filter(subject_identifier=self.recent_infection.subject_identifier)
        self.assertEqual(calls.count(), 1)
        call = calls[0]
        SubjectEligibilityFactory(**self.data)
        self.assertEqual(call.eligibility.registered_subject.subject_identifier, call.subject_identifier)

    def test_next_call_log_available(self):
        call = BcvpCall.objects.get(subject_identifier=self.recent_infection.subject_identifier)
        self.assertEqual(LogEntry.objects.filter(log__call=self).count(), 0)
        self.assertEqual(call.next_call_log[0], Log.objects.get(call=call).id)
