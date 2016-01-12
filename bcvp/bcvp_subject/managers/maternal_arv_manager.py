from django.db import models
from django.db.models import get_model


class MaternalArvManager(models.Manager):

    def get_by_natural_key(self, visit_instance, code, subject_identifier_as_pk):
        MaternalVisit = models.get_model('mb_maternal', 'MaternalVisit')
        maternal_visit = MaternalVisit.objects.get_by_natural_key(visit_instance, code, subject_identifier_as_pk)
        MaternalArvPreg = get_model('mb_maternal', 'MaternalArvPreg')
        maternal_arv_pre = MaternalArvPreg.objects.get_by_natural_key(maternal_visit=maternal_visit)
        return self.get(maternal_arv_pre=maternal_arv_pre)
