from django.utils import timezone
from datetime import date
from dateutil.relativedelta import relativedelta

from edc_appointment.models.appointment import Appointment
from edc_base.utils import edc_base_startup
from edc_constants.constants import YES, NOT_APPLICABLE
from edc_rule_groups.classes.controller import site_rule_groups
from edc_constants.constants import NO

from bcvp.bcvp.app_configuration import AppConfiguration

from .base_test_case import BaseTestCase
from .factories import SubjectEligibilityFactory, SubjectVisitFactory

from ..models import RecentInfection, SubjectConsent
from ..forms import ResidencyMobilityForm
from ..visit_schedule.subject import SubjectVisitSchedule


class TestResidencyMobilityForm(BaseTestCase):

    def setUp(self):
        super(TestResidencyMobilityForm, self).setUp()
        edc_base_startup()
        AppConfiguration().prepare()
        SubjectVisitSchedule().build()
        site_rule_groups.autodiscover()
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
            'length_residence': '1 to 5 years',
            'permanent_resident': YES,
            'intend_residency': NO,
            'nights_away': '1-6 nights',
            'cattle_postlands': 'Farm/lands',
            'cattle_postlands_other': '',
        }

    def test_permanent_residence(self):
        """Assert if resident is permanent(14 nights per month), then cannot stay more than 6 months away."""
        self.data['nights_away'] = 'more than 6 months'
        form = ResidencyMobilityForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'If participant has spent 14 or more nights per month in this community, nights away CANNOT be '
            'more than 6months.', errors)

    def test_cattle_postlands_1(self):
        """Assert if participant spent zero nights away, times spent away should be Not applicable."""
        self.data['nights_away'] = 'zero'
        form = ResidencyMobilityForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'If participant spent zero nights away, times spent away should be Not applicable', errors)

    def test_cattle_postlands_2(self):
        """Assert if participant spent nights away, times spent away cannot be Not applicable."""
        self.data['cattle_postlands'] = NOT_APPLICABLE
        form = ResidencyMobilityForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has spent more than zero nights away, times spent away CANNOT be Not applicable.', errors)
