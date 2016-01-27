import factory
from datetime import date
from django.utils import timezone

from edc_constants.constants import YES, NO
from bcvp.bcvp_subject.models import (SubjectEligibility, RecentInfection, SubjectLocator, SubjectConsent,
                                      SubjectVisit, SubjectRefusal)
from edc_constants.choices import ALIVE
from edc_visit_tracking.tests.factories import TestVisitFactory


class SubjectEligibilityFactory(factory.DjangoModelFactory):

    class Meta:
        model = SubjectEligibility

    report_datetime = timezone.now()
    age_in_years = 26
    has_omang = YES
    willing_to_participate = YES
    survival_status = ALIVE
    first_name = factory.Faker('name')


class RecentInfectionFactory(factory.DjangoModelFactory):

    class Meta:
        model = RecentInfection

    subject_identifier = factory.Sequence(lambda n: '078-88888899-{0}'.format(n))
    first_name = factory.Faker('name')
    dob = date(1980, 01, 01)
    initials = 'AB'
    identity = factory.Sequence(lambda n: '94561987{0}'.format(n))
    specimen_identifier = factory.Sequence(lambda n: '{0}'.format(n))
    test_date = date.today()
    drawn_datetime = timezone.now()
    result = 'result'
    gps_target_lon = factory.Sequence(lambda n: '25.5460{0}'.format(n))
    gps_target_lat = factory.Sequence(lambda n: '-25.3306{0}'.format(n))
    area_name = 'mochudi'
    subject_cell = factory.Sequence(lambda n: '7346589{0}'.format(n))
    subject_cell_alt = factory.Sequence(lambda n: '7566589{0}'.format(n))


class SubjectLocatorFactory(factory.DjangoModelFactory):

    class Meta:
        model = SubjectLocator

    report_datetime = timezone.now()
    may_follow_up = YES
    home_visit_permission = YES
    physical_address = 'near general dealer black gate'
    subject_cell = factory.Sequence(lambda n: '72111{0}'.format(n))
    may_call_work = NO
    may_contact_someone = NO


class SubjectConsentFactory(factory.DjangoModelFactory):

    class Meta:
        model = SubjectConsent


class SubjectRefusalFactory(factory.DjangoModelFactory):

    class Meta:
        model = SubjectRefusal

    refusal_date = date.today()
    reason = 'Fear of needles'


class SubjectVisitFactory(TestVisitFactory):

    class Meta:
        model = SubjectVisit
