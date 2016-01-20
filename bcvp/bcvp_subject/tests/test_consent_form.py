from django.utils import timezone
from datetime import timedelta

from edc_constants.constants import YES, NO, MALE, FEMALE, OMANG

from bcvp.bcvp_subject.models import RecentInfection

from ..forms import SubjectConsentForm

from .base_test_case import BaseTestCase
from .factories import SubjectEligibilityFactory


class TestConsentForm(BaseTestCase):

    def setUp(self):
        super(TestConsentForm, self).setUp()
        self.recent_infection = RecentInfection.objects.first()
        SubjectEligibilityFactory(
            registered_subject=self.recent_infection.registered_subject,
            dob=self.recent_infection.dob,
            initials=self.recent_infection.initials,
            identity=self.recent_infection.identity,
            first_name=self.recent_infection.first_name,
            last_name=self.recent_infection.first_name,
        )
        self.data = {
            'subject_identifier': self.recent_infection.registered_subject.subject_identifier,
            'consent_datetime': timezone.now(),
            'first_name': self.recent_infection.first_name,
            'last_name': self.recent_infection.first_name,
            'initials': self.recent_infection.first_name[:1] + self.recent_infection.first_name[:1],
            'dob': self.recent_infection.dob,
            'is_dob_estimated': NO,
            'gender': MALE,
            'guardian_name': '',
            'consent_reviewed': YES,
            'study_questions': YES,
            'assessment_score': YES,
            'consent_signature': YES,
            'consent_copy': YES,
            'identity_type': OMANG,
            'identity': self.recent_infection.identity,
            'confirm_identity': self.recent_infection.identity,
            'citizen': YES,
            'legal_marriage': '',
            'marriage_certificate': '',
            'marriage_certificate_no': '',
            'is_incarcerated': NO,
            'is_literate': YES,
            'witness_name': '',
            'language': 'en',
        }

    def test_identity_gender(self):
        "Check omang gender digit vs gender"
        self.data['gender'] = FEMALE
        form = SubjectConsentForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Identity provided indicates participant is Male and yet gender is indicated to be Female.', errors)

    def test_match_eligibility_identity(self):
        "Assert that eligibility identity is identical to consent identity"
        self.data['identity'] = '11111111'
        self.data['confirm_identity'] = '11111111'
        form = SubjectConsentForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Identity provided does not match the identity provided in eligibility', errors)

    def test_match_eligibility_first_name(self):
        "Assert that eligibility first-name is identical to eligibility first-name"
        self.data['first_name'] = self.recent_infection.first_name[1:]
        self.data['last_name'] = self.recent_infection.first_name[1:]
        self.data['initials'] = self.data['first_name'][:1] + self.data['first_name'][:1]
        form = SubjectConsentForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'First name does not match first name provided in eligibility', errors)

    def test_match_eligibility_last_name(self):
        "Assert that eligibility last-name is identical to eligibility last-name"
        self.data['last_name'] = self.data['last_name'] + "PERRY"
        form = SubjectConsentForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Last name does not match last name provided in eligibility', errors)

    def test_match_eligibility_dob(self):
        "Assert that eligibility dob is identical to eligibility dob"
        self.data['dob'] = self.data['dob'] - timedelta(days=10)
        form = SubjectConsentForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Date of birth does not match date of birth in eligibility', errors)
