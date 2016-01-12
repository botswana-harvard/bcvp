from django.db import models
from django.db.models import get_model


class AntenatalEnrollmentLossManager(models.Manager):

    def get_by_natural_key(self, registered_subject):
        AntenatalEnrollment = get_model('mb_maternal', 'AntenatalEnrollment')
        antenatal_enrollment = AntenatalEnrollment.objects.get_by_natural_key(
            registered_subject=registered_subject)
        return self.get(antenatal_enrollment=antenatal_enrollment)


class PostnatalEnrollmentLossManager(models.Manager):

    def get_by_natural_key(self, registered_subject):
        PostnatalEnrollment = get_model('mb_maternal', 'PostnatalEnrollment')
        postnatal_enrollment = PostnatalEnrollment.objects.get_by_natural_key(
            registered_subject=registered_subject)
        return self.get(postnatal_enrollment=postnatal_enrollment)
