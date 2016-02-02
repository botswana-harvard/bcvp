from django.utils import timezone

from edc_appointment.models.appointment import Appointment
from edc_constants.constants import YES


from bcvp.bcvp_subject.models import RecentInfection
from bcvp.bcvp_subject.models.subject_consent import SubjectConsent
from bcvp.bcvp_subject.tests.factories import SubjectVisitFactory

from .base_test_case import BaseTestCase
from .factories import SubjectEligibilityFactory

from ..models import SubjectVisit


class TestVisit(BaseTestCase):

    def setUp(self):
        super(TestVisit, self).setUp()
        recent_infection = RecentInfection.objects.first()
        eligibility = SubjectEligibilityFactory(
            registered_subject=recent_infection.registered_subject,
            dob=recent_infection.dob,
            initials=recent_infection.initials,
            identity=recent_infection.identity,
        )
        self.consent = SubjectConsent.objects.create(
            registered_subject=recent_infection.registered_subject,
            study_site='40',
            consent_datetime=timezone.now(),
            identity=eligibility.identity,
            confirm_identity=eligibility.identity,
            is_literate=YES)

    def test_model_save(self):
        appointment = Appointment.objects.get(
            registered_subject=self.consent.registered_subject,
            visit_definition__code='1000')
        SubjectVisitFactory(
            appointment=appointment,
            report_datetime=timezone.now())
        self.assertEqual(SubjectVisit.objects.all().count(), 1)
