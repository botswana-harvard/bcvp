from django.test.testcases import TestCase

from bcvp.bcvp_subject.tests.factories import RecentInfectionFactory
from bcvp.load_edc import load_edc


class BaseTestCase(TestCase):

    def setUp(self):
        load_edc()
        self.study_site = '10'
        RecentInfectionFactory()
        RecentInfectionFactory()
        RecentInfectionFactory()
        RecentInfectionFactory()
