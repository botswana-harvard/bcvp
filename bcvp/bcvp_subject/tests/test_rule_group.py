from django.utils import timezone

from edc_appointment.models import Appointment
from edc_constants.constants import YES, UNKEYED, NOT_REQUIRED, NO
from edc_meta_data.models import CrfMetaData

from .base_test_case import BaseTestCase

from .factories import SubjectEligibilityFactory, SubjectVisitFactory

from ..models import RecentInfection, SubjectConsent, SexualBehaviour


class TestRuleGroup(BaseTestCase):

    def setUp(self):
        super(TestRuleGroup, self).setUp()
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
        self.appointment = Appointment.objects.get(
            registered_subject=consent.registered_subject,
            visit_definition__code='1000')
        self.subject_visit = SubjectVisitFactory(
            appointment=self.appointment,
            report_datetime=timezone.now())

    def test_recent_partner_rule_group_1(self):
        """Assert that if oarticipant is indicated to have no partner in the past three months,
        then recent partner form is not required"""
        SexualBehaviour.objects.create(
            subject_visit=self.subject_visit,
            ever_sex=NO,
            recent_partner=NO
        )
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=NOT_REQUIRED,
            crf_entry__app_label='bcvp_subject',
            crf_entry__model_name='recentpartner',
            appointment=self.appointment
        ).count(), 1)

    def test_recent_partner_rule_group_2(self):
        """Assert that if participant is indicated to have a partner in the past three months
        then recent partner form is required"""
        SexualBehaviour.objects.create(
            subject_visit=self.subject_visit,
            ever_sex=NO,
            recent_partner=YES
        )
        self.assertEqual(CrfMetaData.objects.filter(
            entry_status=UNKEYED,
            crf_entry__app_label='bcvp_subject',
            crf_entry__model_name='recentpartner',
            appointment=self.appointment
        ).count(), 1)
