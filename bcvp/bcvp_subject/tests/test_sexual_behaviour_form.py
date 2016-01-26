from django.utils import timezone

from edc_appointment.models.appointment import Appointment
from edc_base.utils import edc_base_startup
from edc_constants.constants import YES
from edc_rule_groups.classes.controller import site_rule_groups
from edc_constants.constants import NO

from bcvp.bcvp.app_configuration import AppConfiguration

from .base_test_case import BaseTestCase
from .factories import SubjectEligibilityFactory, SubjectVisitFactory

from ..models import RecentInfection, SubjectConsent
from ..forms import SexualBehaviourForm
from ..visit_schedule.subject import SubjectVisitSchedule


class TestSexualBehaviourForm(BaseTestCase):

    def setUp(self):
        super(TestSexualBehaviourForm, self).setUp()
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
            'ever_sex': NO,
            'lifetime_sex_partners': '',
            'last_year_partners': '',
            'more_sex': '',
            'first_sex': '',
            'condom': '',
            'alcohol_sex': '',
        }

    def test_ever__had_sex_vs_partners_1(self):
        """Assert if participant has had sex then sex partner cannot be None."""
        self.data['ever_sex'] = YES
        form = SexualBehaviourForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'If participant has ever had sex, CANNOT have 0 lifetime partners.', errors)

    def test_ever_had_sex_vs_partners_2(self):
        """Assert if participant has had sex then sex partner cannot be None."""
        self.data['ever_sex'] = YES
        self.data['lifetime_sex_partners'] = 0
        form = SexualBehaviourForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'If participant has ever had sex, CANNOT have 0 lifetime partners.', errors)

    def test_ever_had_sex_with_partners_3(self):
        """Assert if participant has never had sex then sex partner greater than 1."""
        self.data['lifetime_sex_partners'] = 5
        form = SexualBehaviourForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'If participant has never had sex, CANNOT have sex partners be greater than 0.', errors)

    def test_ever_had_sex_with_condom_use_1(self):
        """Assert if participant has had sex then should answer question on whether has used a condom."""
        self.data['ever_sex'] = YES
        self.data['lifetime_sex_partners'] = 3
        form = SexualBehaviourForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'If participant has had sex at some point in their life, did participant '
            'use a condom the last time he/she had sex?', errors)

    def test_ever_had_sex_with_condom_use_2(self):
        """Assert if participant has never had sex then should not answer question on whether has used a condom."""
        self.data['condom'] = YES
        form = SexualBehaviourForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has indicated they have never had sex, therefore question on condom use during '
            'sex is not applicable and should be None', errors)

    def test_ever_had_sex_with_alcohol_use_1(self):
        """Assert if participant has had sex then question on sex under alcohol influence should be answered."""
        self.data['ever_sex'] = YES
        self.data['lifetime_sex_partners'] = 3
        self.data['condom'] = YES
        form = SexualBehaviourForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'If participant has had sex at some point in their life, did participant '
            'drink alcohol before sex last time?', errors)

    def test_ever_had_sex_with_alcohol_use_2(self):
        """Assert if participant has never had sex then question on sex under alcohol influence is not applicable."""
        self.data['alcohol_sex'] = 'My partner'
        form = SexualBehaviourForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant has indicated they have never had sex, therefore question on drinking alcohol '
            'during sex is not applicable.', errors)

    def test_past_year_sex_partner_outside_community_1(self):
        self.data['more_sex'] = YES
        form = SexualBehaviourForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'If participant has had sex with somebody living outside of the community in the past year, '
            'CANNOT have 0 last year partners.', errors)

    def test_past_year_sex_partner_outside_community_2(self):
        self.data['more_sex'] = NO
        self.data['last_year_partners'] = 5
        form = SexualBehaviourForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Participant is indicated to have had sex in the past year with someone outside of the community.'
            'Please provide the number of sex partners in the past year.', errors)

    def test_past_year_sex_partners(self):
        self.data['last_year_partners'] = 5
        form = SexualBehaviourForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'If participant has had sex with anyone in the past 12months, has participant '
            'had sex with anyone outside community in the past 12months?', errors)

    def test_partner_numbers(self):
        """Assert that last year sex patrners CONNOT be great than lifetime partners."""
        self.data['ever_sex'] = YES
        self.data['lifetime_sex_partners'] = 3
        self.data['condom'] = YES
        self.data['alcohol_sex'] = 'My partner'
        self.data['more_sex'] = YES
        self.data['last_year_partners'] = 5
        form = SexualBehaviourForm(data=self.data)
        errors = ''.join(form.errors.get('__all__'))
        self.assertIn(
            'Number of partners in the past 12months CANNOT exceed number of life time partners', errors)
