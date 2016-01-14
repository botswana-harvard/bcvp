import factory

from django.utils import timezone

from edc_constants.constants import YES
from bcvp.bcvp_subject.models import SubjectEligibility


class SubjectEligibilityFactory(factory.DjangoModelFactory):

    class Meta:
        model = SubjectEligibility

    report_datetime = timezone.now()
    age_in_years = 26
    has_omang = YES
