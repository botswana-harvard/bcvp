from django.db import models


class RecentInfection(models.Model):

    age_in_years = models.IntegerField(
        verbose_name='What is the age of the participant?')

    objects = models.Manager()

    @property
    def eligibility_matching_dict(self):
        eligibility_matching_attr = {}
        eligibility_matching_attr['age_in_years'] = self.age_in_years
#         eligibility_matching_attr['identity'] = None
#         eligibility_matching_attr['initials'] = None
        return eligibility_matching_attr

    class Meta:
        app_label = 'bcvp_subject'
        verbose_name = 'Recent Infection'
