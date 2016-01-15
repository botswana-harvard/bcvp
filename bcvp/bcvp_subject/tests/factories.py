import factory
from datetime import date
from django.utils import timezone

from edc_constants.constants import YES
from bcvp.bcvp_subject.models import SubjectEligibility, RecentInfection
from edc_constants.choices import ALIVE


class SubjectEligibilityFactory(factory.DjangoModelFactory):

    class Meta:
        model = SubjectEligibility

    report_datetime = timezone.now()
    age_in_years = 26
    has_omang = YES
    willing_to_paticipate = YES
    survival_status = ALIVE


class RecentInfectionFactory(factory.DjangoModelFactory):

    class Meta:
        model = RecentInfection

    subject_identifier = factory.Sequence(lambda n: '078-88888899-{0}'.format(n))
    dob = date(1980, 01, 01)
    initials = 'AB'
    identity = factory.Sequence(lambda n: '34561987{0}'.format(n))
