from django.test.testcases import TestCase
from django.utils import timezone

from bcvp.bcvp_subject.tests.factories import RecentInfectionFactory
from bcvp.load_edc import load_edc


class BaseTestCase(TestCase):

    def setUp(self):
        load_edc()
        self.study_site = '10'
        for _ in range(0, 5):
            RecentInfectionFactory()
