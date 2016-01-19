from django.utils import timezone
from dateutil.relativedelta import relativedelta

from edc_constants.constants import YES, NO, ALIVE, MALE, FEMALE, DEAD
from edc_registration.models.registered_subject import RegisteredSubject

from bcvp.bcvp_subject.models import RecentInfection

from ..forms import SubjectEligibilityForm

from .base_test_case import BaseTestCase


class TestEligibilityForm(BaseTestCase):

    def setUp(self):
        super(TestEligibilityForm, self).setUp()
        self.recent_infection = RecentInfection.objects.first()
        self.data = {
            'registered_subject': self.recent_infection.registered_subject.id,
            'recent_infection': self.recent_infection.id,
            'eligibility_id': None,
            'report_datetime': timezone.now(),
            'first_name': self.recent_infection.first_name,
            'last_name': self.recent_infection.initials,
            'initials': self.recent_infection.initials,
            'gender': MALE,
            'dob': self.recent_infection.dob,
            'age_in_years': relativedelta(timezone.now(), self.recent_infection.dob).years,
            'survival_status': ALIVE,
            'willing_to_participate': YES,
            'has_omang': YES,
            'identity': self.recent_infection.identity,
        }

    def test_identity_gender(self):
        "Check omang gender digit vs gender"
        self.data['gender'] = FEMALE
        form = SubjectEligibilityForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Identity provided indicates participant is Male and yet gender is indicated to be Female.', errors)

    def test_deceased_cannot_be_willing_to_participate(self):
        "Assert that if deceased, willing to participate should not be answered"
        self.data['survival_status'] = DEAD
        form = SubjectEligibilityForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You stated that participant is deceased. Please do not indicate the willingness to participate.', errors)

    def test_alive_fill_willing_to_participate(self):
        "Assert that if alive, willing to participate should be answered"
        self.data['willing_to_participate'] = ''
        form = SubjectEligibilityForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Please indicate the participants willingnes to participate in the study.', errors)
