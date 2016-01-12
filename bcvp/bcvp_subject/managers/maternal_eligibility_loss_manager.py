from django.db import models
from django.db.models import get_model


class MaternalEligibilityLossManager(models.Manager):

    def get_by_natural_key(self, eligibility_id, report_datetime):
        MaternalEligibility = get_model('mb_maternal', 'MaternalEligibility')
        maternal_eligibility = MaternalEligibility.objects.get_by_natural_key(eligibility_id=eligibility_id)
        return self.get(maternal_eligibility=maternal_eligibility, report_datetime=report_datetime)
