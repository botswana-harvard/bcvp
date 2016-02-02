from django.utils import timezone
from datetime import date
from dateutil.relativedelta import relativedelta

from edc_appointment.models.appointment import Appointment
from edc_constants.constants import YES
from edc_constants.constants import NO


from .base_test_case import BaseTestCase
from .factories import SubjectEligibilityFactory, SubjectVisitFactory

from ..models import RecentInfection, SubjectConsent
from ..forms import HivCareAdherenceForm


class TestHivCareAdherenceForm(BaseTestCase):

    def setUp(self):
        super(TestHivCareAdherenceForm, self).setUp()
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
            'first_positive': '',
            'medical_care': '',
            'no_medical_care': '',
            'ever_recommended_arv': '',
            'ever_taken_arv': YES,
            'why_no_arv': '',
            'why_no_arv_other': '',
            'first_arv': date.today() - relativedelta(years=5),
            'on_arv': '',
            'clinic_receiving_from': '',
            'next_appointment_date': '',
            'arv_stop_date': '',
            'arv_stop': NO,
            'arv_stop_other': '',
            'adherence_4_day': '',
            'adherence_4_wk': '',
            'arv_evidence': '',
        }

    def test_first_positive_1(self):
        self.data['first_positive'] = date.today()
        form = HivCareAdherenceForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'First HIV result was provided please answer question on whether HIV related medical or clinical care.',
            errors)

    def test_first_positive_2(self):
        self.data['first_positive'] = date.today()
        self.data['medical_care'] = NO
        form = HivCareAdherenceForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'First HIV result was provided please answer question on recommendation to start ARV by healthworker.',
            errors)

    def test_no_medical_care_1(self):
        self.data['first_positive'] = date.today()
        self.data['medical_care'] = NO
        self.data['ever_recommended_arv'] = NO
        form = HivCareAdherenceForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You have indicated that NO HIV related medical or clinical care was taken.',
            errors)

    def test_no_medical_care_2(self):
        self.data['first_positive'] = date.today()
        self.data['medical_care'] = YES
        self.data['no_medical_care'] = 'Did not feel sick'
        self.data['ever_recommended_arv'] = NO
        form = HivCareAdherenceForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You have indicated that HIV related medical or clinical care was received.',
            errors)

    def test_ever_taken_arv_1(self):
        """Assert that when participant is indicated to have never taken ARV, then reason why not
        taken should not be provided."""
        self.data['ever_taken_arv'] = NO
        form = HivCareAdherenceForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('You have indicated that ARVs were NOT taken.', errors)

    def test_ever_taken_arv_2(self):
        """Assert that when participant is indicated to have ever taken ARV then first arv date is required."""
        self.data['ever_taken_arv'] = YES
        self.data['first_arv'] = ''
        form = HivCareAdherenceForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Please indicate ARV start date.', errors)

    def test_on_arv_must_show_evidence(self):
        """Assert that if currently on ARV, then must indicate if there is evidence"""
        self.data['on_arv'] = YES
        form = HivCareAdherenceForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('Please indicate if there is evidence.', errors)

    def test_not_on_arv_no_evidence(self):
        """Assert that if currently on ARV, then must indicate if there is evidence"""
        self.data['on_arv'] = NO
        self.data['arv_evidence'] = NO
        form = HivCareAdherenceForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('do not indicate whether there evidence participant is on therapy exists', errors)

    def test_never_taken_arv_no_stop_date(self):
        """Assert that if currently not on ARV, then must indicate stop date"""
        self.data['ever_taken_arv'] = NO
        self.data['why_no_arv'] = 'Did not feel sick'
        self.data['arv_stop_date'] = date.today()
        self.data['arv_stop'] = 'Dont like pills'
        self.data['first_arv'] = ''
        form = HivCareAdherenceForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn('If patient has never taken ARV, there cannot be an ARV stop date.', errors)

    def test_on_arv_stop_date(self):
        """Assert that if currently on ARV, then stop date must not be provided"""
        self.data['on_arv'] = YES
        self.data['arv_evidence'] = NO
        self.data['clinic_receiving_from'] = 'BH3'
        self.data['arv_stop_date'] = date.today()
        form = HivCareAdherenceForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You have indicated participant is currently on ARV yet provided an ARV stop date. Please correct.', errors)

    def test_stop_date_no_reason(self):
        """Assert that if ARV stopped, then reason must be provided"""
        self.data['arv_stop_date'] = date.today()
        self.data['arv_stop'] = 'Dont like pills'
        form = HivCareAdherenceForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'You have indicated participant has stopped ARV, please provide a reason', errors)

#     def test_no_stop_date_stop_reason_given(self):
#         """Assert that if ARV not stopped, then reason must not be provided"""
#         self.data['arv_stop'] = 'Dont like pills'
#         form = HivCareAdherenceForm(data=self.data)
#         errors = ''.join(form.errors.get('__all__'))
#         self.assertIn(
#            'You have indicated participant has not stopped ARV, please do not provide a reason why ARV were stopped.',
#            errors)

    def test_missed_doses(self):
        """Assert that if currently on ARV cannot indicate missed doses in past four days"""
        self.data['on_arv'] = YES
        self.data['first_positive'] = date.today()
        self.data['no_medical_care'] = 'Did not feel sick'
        self.data['medical_care'] = NO
        self.data['ever_recommended_arv'] = NO
        self.data['arv_evidence'] = NO
        self.data['clinic_receiving_from'] = 'BH3'
        form = HivCareAdherenceForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'If patient is on ARV, please provide missed doses in past four days.',
            errors)

    def test_adherence(self):
        """Assert that if currently on ARV cannot indicate adherence info"""
        self.data['on_arv'] = YES
        self.data['first_positive'] = date.today()
        self.data['no_medical_care'] = 'Did not feel sick'
        self.data['medical_care'] = NO
        self.data['ever_recommended_arv'] = NO
        self.data['arv_evidence'] = NO
        self.data['clinic_receiving_from'] = 'BH3'
        self.data['adherence_4_day'] = 'One day'
        form = HivCareAdherenceForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'If patient is on ARV, please provide information on ability to take medications as prescribed.',
            errors)
