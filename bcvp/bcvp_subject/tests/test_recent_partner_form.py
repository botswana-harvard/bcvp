from django.utils import timezone

from edc_appointment.models.appointment import Appointment
from edc_constants.constants import YES, FEMALE, UNKNOWN, POS


from .base_test_case import BaseTestCase
from .factories import SubjectEligibilityFactory, SubjectVisitFactory

from ..models import RecentInfection, SubjectConsent
from ..forms import RecentPartnerForm


class TestRecentPartnerForm(BaseTestCase):

    def setUp(self):
        super(TestRecentPartnerForm, self).setUp()
        recent_infection = RecentInfection.objects.first()
        eligibility = SubjectEligibilityFactory(
            registered_subject=recent_infection.registered_subject,
            dob=recent_infection.dob,
            initials=recent_infection.initials,
            identity=recent_infection.identity,
        )
        consent = SubjectConsent.objects.create(
            registered_subject=recent_infection.registered_subject,
            study_site='40',
            consent_datetime=timezone.now(),
            identity=eligibility.identity,
            confirm_identity=eligibility.identity,
            is_literate=YES,
            dob=recent_infection.dob,)
        appointment = Appointment.objects.get(
            registered_subject=consent.registered_subject,
            visit_definition__code='1000')
        subject_visit = SubjectVisitFactory(
            appointment=appointment,
            report_datetime=timezone.now())
        self.data = {
            'subject_visit': subject_visit.id,
            'report_datetime': timezone.now(),
            'rel_type': 'Casual',
            'partner_residency': 'In this community',
            'partner_age': 20,
            'partner_gender': FEMALE,
            'last_sex_contact': 0,
            'last_sex_period': '',
            'first_sex_contact': 0,
            'first_sex_period': '',
            'regular_sex': 0,
            'having_sex': '',
            'having_sex_reg': 'Sometimes',
            'alcohol_before_sex': YES,
            'partner_status': UNKNOWN,
            'partner_arv': '',
            'status_disclosure': '',
            'multiple_partners': '',
            'intercourse_type': '',
        }

    def test_last_sex_1(self):
        """Assert if last sex contact is greater than 0, then should indicate the period."""
        self.data['last_sex_contact'] = 5
        form = RecentPartnerForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Please indicate whether the last sex period is in days, months or years.', errors)

    def test_last_sex_2(self):
        """Assert if last sex contact is 0, then period should not be filled."""
        self.data['last_sex_period'] = 'days'
        form = RecentPartnerForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Please do not provide the period that has past since the last sex as it is indicated to be 0.', errors)

    def test_first_sex_1(self):
        """Assert if last sex contact is greater than 0, then should indicate the period."""
        self.data['first_sex_contact'] = 5
        form = RecentPartnerForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Please indicate whether the first sex period is in days, months or years.', errors)

    def test_first_sex_2(self):
        """Assert if last sex contact is 0, then period should not be filled."""
        self.data['first_sex_period'] = 'days'
        form = RecentPartnerForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Please do not provide the period that has past since the first sex with this person as it is '
            'indicated to be 0.', errors)

    def test_partner_status_1(self):
        """Assert that if partner status is positive then should fill data on ARV"""
        self.data['partner_status'] = POS
        form = RecentPartnerForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You indicated partner status is Positive. Please indicate whether they are on ARV.', errors)

    def test_partner_status_2(self):
        """Assert that if partner status is not positive then should not fill question on ARV"""
        self.data['partner_arv'] = YES
        form = RecentPartnerForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'question on whether he/she is taking antiretrovirals should be None', errors)
