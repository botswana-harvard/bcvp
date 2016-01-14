from django.test.testcases import TestCase

from bcvp.load_edc import load_edc


class BaseTestCase(TestCase):

    def setUp(self):
        load_edc()
        self.study_site = '10'
