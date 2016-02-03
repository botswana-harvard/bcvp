from datetime import datetime

from django.utils import timezone

from edc_constants.constants import YES, NO, ALIVE, CLOSED, NEW
from edc_constants.choices import TIME_OF_DAY, TIME_OF_WEEK
from edc_call_manager.models import Log, LogEntry
from edc_call_manager.choices import CONTACT_TYPE

from bcvp.bcvp_subject.models import (RecentInfection, BcvpCall)

from .base_test_case import BaseTestCase
from .factories import SubjectEligibilityFactory
from bcvp.bcvp_subject.forms.subject_locator_form import SubjectLocatorForm


class TestSubjectLocatorForm(BaseTestCase):

    def setUp(self):
        super(TestSubjectLocatorForm, self).setUp()
        recent_infection = RecentInfection.objects.first()
        eligibility = SubjectEligibilityFactory(
            registered_subject=recent_infection.registered_subject,
            dob=recent_infection.dob,
            initials=recent_infection.initials,
            identity=recent_infection.identity,
        )
        call = BcvpCall.objects.get(
            subject_identifier=recent_infection.registered_subject.subject_identifier,
            call_status=NEW)
        self.log = Log.objects.get(call=call)
        call = LogEntry.objects.create(
            log=self.log,
            call_datetime=timezone.now(),
            contact_type='direct',
            survival_status=ALIVE,
            call_again=NO)
        self.data = {
            'registered_subject': YES,
            'report_datetime': timezone.now(),
            'mail_address': '',
            'home_visit_permission': NO,
            'physical_address': '',
            'may_follow_up': NO,
            'may_sms_follow_up': NO,
            'subject_cell': '',
            'subject_cell_alt': '',
            'may_call_work': NO,
            'subject_work_place': '',
            'subject_work_phone': '',
            'may_contact_someone': NO,
            'contact_name': '',
            'contact_rel': '',
            'contact_physical_address': '',
            'successful_mode_of_contact': 'telephone',
        }

    def test_eligibility_confirm_appointment_1(self):
        """Assert that if appointment was not scheduled through a call then successful mode of contact as telephone
        is not valid"""
        form = SubjectLocatorForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'On the call log entry it was indicated that an appointment was not scheduled.', errors)

    def test_eligibility_confirm_appointment_2(self):
        """Assert that if appointment was not schedule through a call then successful mode of contact as
        household visit is valid."""
        self.data['successful_mode_of_contact'] = 'household_visit'
        form = SubjectLocatorForm(data=self.data)
        form.is_valid()
