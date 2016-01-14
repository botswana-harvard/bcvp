from django.test.testcases import TestCase

from bcvp.bcvp_subject.models import RecentInfection
from bcvp.load_edc import load_edc


class BaseTestCase(TestCase):

    def setUp(self):
        load_edc()
        self.study_site = '10'
        RecentInfection.objects.create(age_in_years=20)
        RecentInfection.objects.create(age_in_years=21)
        RecentInfection.objects.create(age_in_years=22)
        RecentInfection.objects.create(age_in_years=23)
