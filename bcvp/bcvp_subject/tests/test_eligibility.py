from edc_constants.constants import SCREENED
from edc_registration.models.registered_subject import RegisteredSubject
from edc_constants.constants import DEAD, YES, NO

from bcvp.bcvp_subject.models import (SubjectEligibility, RecentInfection, SubjectEligibilityLoss,
                                      SubjectRefusalReport)


from ..exceptions import NoMatchingRecentInfectionException
from .base_test_case import BaseTestCase
from .factories import SubjectEligibilityFactory


class TestEligibility(BaseTestCase):

    def test_eligibility_who_has_omang(self):
        """Test eligibility of a subject with an Omang."""
        options = {'has_omang': 'Yes'}
        reference_record = RecentInfection.objects.first()
        options.update(**reference_record.eligibility_matching_dict)
        subject_eligibility = SubjectEligibilityFactory(**options)
        self.assertTrue(subject_eligibility.is_eligible)

    def test_eligibility_who_has_no_omang(self):
        """Test eligibility of a subject with no Omang."""
        options = {'has_omang': 'No'}
        reference_record = RecentInfection.objects.first()
        options.update(**reference_record.eligibility_matching_dict)
        subject_eligibility = SubjectEligibilityFactory(**options)
        self.assertFalse(subject_eligibility.is_eligible)

    def test_updates_registered_subject_on_add(self):
        options = {'age_in_years': 26}
        reference_record = RecentInfection.objects.first()
        options.update(**reference_record.eligibility_matching_dict)
        self.assertEqual(RegisteredSubject.objects.all().count(), 0)
        subject_eligibility = SubjectEligibilityFactory(**options)
        subject_eligibility = SubjectEligibility.objects.get(pk=subject_eligibility.pk)
        self.assertTrue(subject_eligibility.is_eligible)
        registered_subject = RegisteredSubject.objects.get(pk=subject_eligibility.registered_subject.pk)
        self.assertEquals(registered_subject.screening_datetime, subject_eligibility.report_datetime)
        self.assertEquals(registered_subject.registration_status, SCREENED)

    def test_updates_registered_subject_on_edit(self):
        options = {'age_in_years': 26}
        reference_record = RecentInfection.objects.first()
        options.update(**reference_record.eligibility_matching_dict)
        self.assertEqual(RegisteredSubject.objects.all().count(), 0)
        subject_eligibility = SubjectEligibilityFactory(**options)
        self.assertTrue(subject_eligibility.is_eligible)
        subject_eligibility.age_in_years = 27
        subject_eligibility.save()
        registered_subject = RegisteredSubject.objects.get(screening_identifier=subject_eligibility.eligibility_id)
        self.assertEquals(registered_subject.screening_age_in_years, 27)
        self.assertEquals(registered_subject.registration_status, SCREENED)

    def test_can_match_eligibility_in_reference_table(self):
        """Asserts that an enrollment instance can correctly reverse match its existing recent infection record"""
        # Recent infection record already exists
        reference_record = RecentInfection.objects.first()
        # Create an enrollment record using criteria for an existing recent infection record
        enrollment = SubjectEligibilityFactory(**reference_record.eligibility_matching_dict)
        self.assertTrue(enrollment.recent_infection_record)

    def test_can_match_registeredsubject_to_reference_table(self):
        """Asserts that an existing instance of registered subject can correctly reverse match its existing
        recent infection record"""
        # Recent infection record already exists
        reference_record = RecentInfection.objects.first()
        # Create an enrollment record using criteria for an existing recent infection record
        SubjectEligibilityFactory(**reference_record.eligibility_matching_dict)
        self.assertTrue(RegisteredSubject.objects.filter(subject_identifier=reference_record.subject_identifier))

    def test_exception_no_match_in_reference_table(self):
        """Asserts that an enrollment instance will throw exception if failing to match recent infection record"""
        # Use a random criteria that will not match any record in recent infections table
        eligibility_matching_dict = {}
        with self.assertRaises(NoMatchingRecentInfectionException):
            SubjectEligibilityFactory(**eligibility_matching_dict)

    def test_creating_enrollment_loss(self):
        """Asserts enrollment loss is created when eligibility is failed."""
        options = {'has_omang': 'No'}
        reference_record = RecentInfection.objects.first()
        options.update(**reference_record.eligibility_matching_dict)
        subject_eligibility = SubjectEligibilityFactory(**options)
        self.assertFalse(subject_eligibility.is_eligible)
        self.assertEqual(SubjectEligibilityLoss.objects.filter(subject_eligibility=subject_eligibility).count(), 1)

    def test_creating_refusal_status(self):
        """Asserts refusal record is created when eligibility is failed by REFUSAL, with refusal reason and
        date being null, awaiting to be updated."""
        options = {'willing_to_paticipate': NO}
        reference_record = RecentInfection.objects.first()
        options.update(**reference_record.eligibility_matching_dict)
        subject_eligibility = SubjectEligibilityFactory(**options)
        self.assertFalse(subject_eligibility.is_eligible)
        refusal_report = SubjectRefusalReport.objects.filter(subject_eligibility=subject_eligibility)
        self.assertTrue(refusal_report.exists())
        self.assertIsNone(refusal_report[0].reason)
        self.assertIsNone(refusal_report[0].refusal_date)

    def test_resetting_refusal_status(self):
        """Asserts refusal and loss records are deleted when eligibility from a previous refusal to participate."""
        options = {'willing_to_paticipate': NO}
        reference_record = RecentInfection.objects.first()
        options.update(**reference_record.eligibility_matching_dict)
        subject_eligibility = SubjectEligibilityFactory(**options)
        self.assertFalse(subject_eligibility.is_eligible)
        refusal_report = SubjectRefusalReport.objects.filter(subject_eligibility=subject_eligibility)
        self.assertTrue(refusal_report.exists())
        subject_eligibility.willing_to_paticipate = YES
        subject_eligibility.save()
        self.assertTrue(subject_eligibility.is_eligible)
        refusal_report = SubjectRefusalReport.objects.filter(subject_eligibility=subject_eligibility)
        self.assertFalse(refusal_report.exists())
