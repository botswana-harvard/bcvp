from django.db import models


class MaternalPostMedItemsManager(models.Manager):

    def get_by_natural_key(self, report_datetime, visit_instance, appt_status,
                           visit_definition_code, subject_identifier_as_pk):
        MaternalVisit = models.get_model('mb_maternal', 'MaternalVisit')
        MaternalPostFuMed = models.get_model('mb_maternal', 'MaternalPostFuMed')
        maternal_visit = MaternalVisit.objects.get_by_natural_key(
            report_datetime, visit_instance, appt_status, visit_definition_code, subject_identifier_as_pk)
        maternal_post_med = MaternalPostFuMed.objects.get(maternal_visit=maternal_visit)
        return self.get(maternal_post_med=maternal_post_med)
