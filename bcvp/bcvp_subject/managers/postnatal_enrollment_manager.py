from django.db import models
from django.db.models import get_model


class PostnatalEnrollmentManager(models.Manager):

    def get_by_natural_key(self, report_datetime, subject_identifier_as_pk):
        RegisteredSubject = get_model('registration', 'RegisteredSubject')
        registered_subject = RegisteredSubject.objects.get_by_natural_key(subject_identifier_as_pk)
        return self.get(report_datetime=report_datetime, registered_subject=registered_subject)
