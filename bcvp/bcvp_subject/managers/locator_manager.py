from django.db import models


class LocatorManager(models.Manager):

    def get_by_natural_key(self, registered_subject):
        return self.get(registered_subject=registered_subject)
