from django.test.testcases import TestCase

from edc_rule_groups.classes.controller import site_rule_groups
from edc_lab.lab_profile.classes.controller import site_lab_profiles
from edc_lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile

from bcvp.bcvp_lab.lab_profiles import SubjectProfile
from bcvp.bcvp.app_configuration import AppConfiguration
from bcvp.bcvp_subject.visit_schedule import SubjectVisitSchedule


class BaseTestCase(TestCase):

    def setUp(self):
        try:
            site_lab_profiles.register(SubjectProfile())
        except AlreadyRegisteredLabProfile:
            pass
        AppConfiguration(lab_profiles=site_lab_profiles).prepare()
        SubjectVisitSchedule().build()
        site_rule_groups.autodiscover()
        self.study_site = '10'
