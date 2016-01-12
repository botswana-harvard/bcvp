from django.db import models


class MaternalEligibilityManager(models.Manager):

    def get_by_natural_key(self, eligibility_id, report_datetime):
        return self.get(eligibility_id=eligibility_id, report_datetime=report_datetime)
