from edc_constants.constants import SCREENED
from edc_registration.models.registered_subject import RegisteredSubject

from bcvp.bcvp_subject.models import SubjectEligibility

from .base_test_case import BaseTestCase
from .factories import SubjectEligibilityFactory


class TestEligibility(BaseTestCase):

    def test_eligibility_who_has_omang(self):
        """Test eligibility of a subject with an Omang."""
        options = {'has_omang': 'Yes'}
        subject_eligibility = SubjectEligibilityFactory(**options)
        self.assertTrue(subject_eligibility.is_eligible)

    def test_eligibility_who_has_no_omang(self):
        """Test eligibility of a subject with no Omang."""
        options = {'has_omang': 'No'}
        subject_eligibility = SubjectEligibilityFactory(**options)
        self.assertFalse(subject_eligibility.is_eligible)

    def test_updates_registered_subject_on_add(self):
        options = {'age_in_years': 26}
        self.assertEqual(RegisteredSubject.objects.all().count(), 0)
        subject_eligibility = SubjectEligibilityFactory(**options)
        subject_eligibility = SubjectEligibility.objects.get(pk=subject_eligibility.pk)
        self.assertTrue(subject_eligibility.is_eligible)
        registered_subject = RegisteredSubject.objects.get(pk=subject_eligibility.registered_subject.pk)
        self.assertEquals(registered_subject.screening_datetime, subject_eligibility.report_datetime)
        self.assertEquals(registered_subject.registration_status, SCREENED)

    def test_updates_registered_subject_on_edit(self):
        options = {'age_in_years': 26}
        self.assertEqual(RegisteredSubject.objects.all().count(), 0)
        subject_eligibility = SubjectEligibilityFactory(**options)
        self.assertTrue(subject_eligibility.is_eligible)
        subject_eligibility.age_in_years = 27
        subject_eligibility.save()
        registered_subject = RegisteredSubject.objects.get(screening_identifier=subject_eligibility.eligibility_id)
        self.assertEquals(registered_subject.screening_age_in_years, 27)
        self.assertEquals(registered_subject.registration_status, SCREENED)
