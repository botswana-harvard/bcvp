from django.test.testcases import TestCase

from edc_configuration.convert import localize
from edc_configuration.models import GlobalConfiguration
from edc_configuration.defaults import default_global_configuration
from edc_lab.lab_profile.classes import site_lab_profiles

from bcvp.bcvp.app_configuration import AppConfiguration, study_end_datetime, study_start_datetime

site_lab_profiles.autodiscover()


class TestConfiguration(TestCase):

    def test_reads_global_config(self):
        """Assert a value specified in the local app overwrites the default."""
        self.assertEqual(default_global_configuration.get('appointment').get('allowed_iso_weekdays'), '1234567')
        self.assertEqual(default_global_configuration.get('appointment').get('default_appt_type'), 'default')
        self.assertEqual(default_global_configuration.get('appointment').get('use_same_weekday'), True)
        AppConfiguration(lab_profiles=site_lab_profiles).prepare()
        self.assertEqual(GlobalConfiguration.objects.get_attr_value('default_appt_type'), 'clinic')
        self.assertEqual(GlobalConfiguration.objects.get_attr_value('use_same_weekday'), True)
        self.assertEqual(GlobalConfiguration.objects.get_attr_value('allowed_iso_weekdays'), '12345')

    def test_prepare(self):
        AppConfiguration(lab_profiles=site_lab_profiles).prepare()
        self.assertEqual(GlobalConfiguration.objects.get_attr_value('default_appt_type'), 'clinic')
        self.assertEqual(GlobalConfiguration.objects.get_attr_value('use_same_weekday'), True)
        self.assertEqual(GlobalConfiguration.objects.get_attr_value('appointments_days_forward'), 15)
        self.assertEqual(GlobalConfiguration.objects.get_attr_value('allowed_iso_weekdays'), '12345')
        self.assertEqual(
            GlobalConfiguration.objects.get_attr_value('start_datetime'),
            localize(study_start_datetime))
        self.assertEqual(
            GlobalConfiguration.objects.get_attr_value('end_datetime'),
            localize(study_end_datetime))
