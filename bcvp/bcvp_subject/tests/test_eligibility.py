from edc_constants.constants import SCREENED, YES, NO, ALIVE
from edc_registration.models.registered_subject import RegisteredSubject
from edc_call_manager.models import Call
from bcvp.bcvp_subject.models import (
    RecentInfection, SubjectEligibilityLoss, SubjectRefusal)


from ..exceptions import NoMatchingRecentInfectionException

from .base_test_case import BaseTestCase
from .factories import SubjectEligibilityFactory
from django.core.exceptions import ObjectDoesNotExist
from bcvp.bcvp_subject.tests.factories import RecentInfectionFactory
from bcvp.bcvp_subject.models.subject_locator import SubjectLocator


class TestEligibility(BaseTestCase):

    def setUp(self):
        super(TestEligibility, self).setUp()
        self.recent_infection = RecentInfection.objects.first()
        self.data = {
            'dob': self.recent_infection.dob,
            'has_omang': YES,
            'identity': self.recent_infection.identity,
            'initials': self.recent_infection.initials,
            'survival_status': ALIVE,
            'willing_to_participate': YES}

    def test_recent_infection_creates_registered_subject(self):
        RecentInfectionFactory(subject_identifier='1234')
        self.assertEqual(RegisteredSubject.objects.filter(subject_identifier='1234').count(), 1)

    def test_recent_infection_updates_registered_subject(self):
        recent_infection = RecentInfectionFactory(subject_identifier='1234')
        recent_infection.first_name = 'ERIK'
        recent_infection.save()
        self.assertEqual(RegisteredSubject.objects.filter(subject_identifier='1234', first_name='ERIK').count(), 1)

    def test_recent_infection_creates_subject_locator(self):
        recent_infection = RecentInfectionFactory(subject_identifier='1234')
        self.assertEqual(SubjectLocator.objects.filter(
            registered_subject=recent_infection.registered_subject).count(), 1)

    def test_recent_infection_updates_subject_locator(self):
        recent_infection = RecentInfectionFactory(subject_identifier='1234')
        recent_infection.subject_cell = '72331115'
        recent_infection.save()
        self.assertEqual(SubjectLocator.objects.filter(
            registered_subject=recent_infection.registered_subject,
            subject_cell='72331115').count(), 1)

    def test_recent_infection_creates_call(self):
        """Assert creates one Call per Recent Infection"""
        recent_infections = RecentInfection.objects.all().count()
        calls = Call.objects.all().count()
        self.assertEqual(calls, recent_infections)
        RecentInfectionFactory(subject_identifier='1234')
        self.assertFalse(RecentInfection.objects.all().count() != Call.objects.all().count())

    def test_eligibility_who_has_omang(self):
        """Assert eligibility of a subject with an Omang."""
        self.data.update({'has_omang': YES})
        subject_eligibility = SubjectEligibilityFactory(**self.data)
        self.assertTrue(subject_eligibility.is_eligible)

    def test_eligibility_who_has_no_omang(self):
        """Assert ineligible if no Omang."""
        self.data.update({'has_omang': NO})
        subject_eligibility = SubjectEligibilityFactory(**self.data)
        self.assertFalse(subject_eligibility.is_eligible)

    def test_updates_registered_subject_on_add(self):
        self.data.update({'age_in_years': 26})
        subject_eligibility = SubjectEligibilityFactory(**self.data)
        self.assertTrue(subject_eligibility.is_eligible)
        registered_subject = RegisteredSubject.objects.get(pk=subject_eligibility.registered_subject.pk)
        self.assertEquals(registered_subject.screening_datetime.date(), subject_eligibility.report_datetime.date())
        self.assertEquals(registered_subject.registration_status, SCREENED)

#     def test_updates_registered_subject_on_edit(self):
#         """dob and age don't correspond...."""
#         self.data.update({'age_in_years': 26})
#         registered_subject = RegisteredSubject.objects.first()
#         subject_eligibility = SubjectEligibilityFactory(
#             registered_subject=registered_subject, **self.data)
#         self.assertTrue(subject_eligibility.is_eligible)
#         self.assertEquals(registered_subject.screening_age_in_years, 26)
#         subject_eligibility.age_in_years = 27
#         subject_eligibility.save()
#         registered_subject = RegisteredSubject.objects.get(
#             screening_identifier=subject_eligibility.pk)
#         self.assertEquals(registered_subject.screening_age_in_years, 27)

    def test_can_match_eligibility_in_reference_table(self):
        """Assert SubjectEligibility.recent_infection is set correctly."""
        subject_eligibility = SubjectEligibilityFactory(**self.data)
        self.assertEqual(subject_eligibility.recent_infection.pk, self.recent_infection.pk)

    def test_can_match_registeredsubject_to_reference_table(self):
        """Assert subject identifier in RecentInfection is correctly transcribed to RegisteredSubject."""
        SubjectEligibilityFactory(**self.data)
        self.assertTrue(
            RegisteredSubject.objects.filter(
                subject_identifier=self.recent_infection.subject_identifier))

    def test_exception_no_match_in_reference_table(self):
        """Assert that SubjectEligibility instance raises an exception
        if failing to match recent infection record"""
        self.data.update({'identity': '987654321'})
        with self.assertRaises(NoMatchingRecentInfectionException):
            SubjectEligibilityFactory(**self.data)

    def test_create_eligibility_loss(self):
        """Assert SubjectEligibilityLoss is created when eligibility fails."""
        self.data.update({'has_omang': NO})
        subject_eligibility = SubjectEligibilityFactory(**self.data)
        self.assertFalse(subject_eligibility.is_eligible)
        self.assertEqual(
            SubjectEligibilityLoss.objects.filter(
                subject_eligibility=subject_eligibility).count(), 1)

    def test_creating_refusal_status(self):
        """Assert refusal record is created when eligibility fails
        reason=REFUSAL, with refusal reason and date being null,
        awaiting to be updated."""
        self.data.update({'willing_to_participate': NO})
        subject_eligibility = SubjectEligibilityFactory(**self.data)
        self.assertFalse(subject_eligibility.is_eligible)
        with self.assertRaises(ObjectDoesNotExist):
            try:
                subject_refusal = SubjectRefusal.objects.get(
                    subject_eligibility=subject_eligibility)
            except ObjectDoesNotExist:
                pass
            else:
                raise ObjectDoesNotExist
        self.assertIsNone(subject_refusal.reason)
        self.assertIsNone(subject_refusal.refusal_date)

    def test_unwilling_deletes_subject_refusal(self):
        """Asserts refusal and loss records are deleted when eligibility from a previous refusal to participate."""
        self.data.update({'willing_to_participate': NO})
        subject_eligibility = SubjectEligibilityFactory(**self.data)
        self.assertFalse(subject_eligibility.is_eligible)
        subject_eligibility.willing_to_participate = YES
        subject_eligibility.save()
        self.assertTrue(subject_eligibility.is_eligible)
        with self.assertRaises(ObjectDoesNotExist):
                SubjectRefusal.objects.get(subject_eligibility=subject_eligibility)
